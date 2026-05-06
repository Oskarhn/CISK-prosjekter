#define F_CPU 1000000UL
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
#include <util/delay.h>
#include <stdint.h>
#include "lcd.h"
#include "i2c.h"

#define STATE_DISARMED  0
#define STATE_ARMED     1
#define STATE_ALARM     2

volatile uint8_t  touch_flag     = 0;
volatile uint8_t  touch_debounce = 0;
volatile uint16_t ms             = 0;

ISR(INT0_vect)
{
    if (!touch_debounce) { touch_flag = 1; touch_debounce = 50; }
}

static void send_to_slaves(uint8_t cmd)
{
    I2C_Master_Send(SLAVE1_ADDR, cmd);
    _delay_ms(5);
    I2C_Master_Send(SLAVE2_ADDR, cmd);
}

static void lcd_update(uint8_t state)
{
    switch (state)
    {
        case STATE_DISARMED:
            LCD_String_xy(0, 0, "  IKKE ARMERT   ");
            LCD_String_xy(1, 0, "Trykk for ARMERE");
            break;
        case STATE_ARMED:
            LCD_String_xy(0, 0, "    ARMERT      ");
            LCD_String_xy(1, 0, "    HUS: OK     ");
            break;
        case STATE_ALARM:
            LCD_String_xy(0, 0, "  !! ALARM !!   ");
            LCD_String_xy(1, 0, "  HUS: IKKE OK  ");
            break;
    }
}

ISR(TIMER0_COMP_vect)
{
    static uint8_t  system_state = STATE_DISARMED;
    static uint16_t last_poll    = 0;

    ms++;
    if (touch_debounce) touch_debounce--;

    /* Touch: endre tilstand og varsle slaver */
    if (touch_flag)
    {
        touch_flag = 0;
        switch (system_state)
        {
            case STATE_DISARMED:
                system_state = STATE_ARMED;
                send_to_slaves(CMD_ARMED);
                break;
            default: 
                system_state = STATE_DISARMED;
                send_to_slaves(CMD_DISARMED);
                break;
        }
        lcd_update(system_state);
    }

    /* Poll slave 1 hvert 500ms naar armert */
    if (system_state == STATE_ARMED && (uint16_t)(ms - last_poll) >= 500)
    {
        last_poll = ms;
        if (I2C_Master_Read(SLAVE1_ADDR) == STATUS_DOOR_OPEN)
        {
            system_state = STATE_ALARM;
            send_to_slaves(CMD_ALARM);
            lcd_update(system_state);
        }
    }
}

int main(void)
{
    DDRD  &= ~(1 << PD2);
    PORTD &= ~(1 << PD2);
    MCUCR |= (1 << ISC01) | (1 << ISC00);
    GICR  |= (1 << INT0);

    TCCR0  = (1 << WGM01) | (1 << CS01);
    OCR0   = 124;
    TIMSK |= (1 << OCIE0);

    LCD_Init();
    I2C_Master_Init();
    sei();

    LCD_String_xy(0, 0, "Smarthus Alarm  ");
    LCD_String_xy(1, 0, "Starter opp...  ");
    _delay_ms(1500);
    lcd_update(STATE_DISARMED);

    set_sleep_mode(SLEEP_MODE_IDLE);

    while (1)
    {
        sleep_mode();
        }
        return 0;
}
