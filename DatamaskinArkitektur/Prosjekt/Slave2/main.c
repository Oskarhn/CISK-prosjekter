/*
 * main.c - Slave 2: I2C + buzzer + LEDs
 * ATmega32 @ 1MHz, I2C adresse: 0x20
 *
 * PB0 : Roed LED
 * PB1 : Gul LED
 * PD5 : Passiv buzzer
 * PC0/PC1 : I2C SCL/SDA
 *
 * All logikk kjoerer i TIMER0_COMP ISR - while-loopen er tom (sleep_mode).
 *   TIMER0_COMP: ms-teller, melodioppdatering, I2C-poll, LED-blink
 */

#define F_CPU 1000000UL
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
#include <stdint.h>
#include "i2c.h"
#include "buzzer.h"

#define STATE_DISARMED  0
#define STATE_ARMED     1
#define STATE_ALARM     2

volatile uint16_t ms         = 0;
volatile uint8_t  buzzer_paa = 0;

ISR(TIMER0_COMP_vect)
{
    static uint8_t  siren_tick   = 0;
    static uint8_t  system_state = STATE_DISARMED;
    static uint8_t  rx_cmd       = 0;
    static uint8_t  led_state    = 0;
    static uint16_t last_blink   = 0;

    ms++;

    /* Melodioppdatering hvert 50ms naar buzzer er paa */
    if (buzzer_paa && ++siren_tick >= 50)
        { siren_tick = 0; Buzzer_Melody_Update(); }

    /* I2C: ta imot kommando fra master */
    if (I2C_Slave_Poll(&rx_cmd, STATUS_OK) == 1)
    {
        switch (rx_cmd)
        {
            case CMD_DISARMED:
                system_state = STATE_DISARMED;
                buzzer_paa   = 0;
                Buzzer_Off();
                PORTB       &= ~((1 << PB0) | (1 << PB1));
                led_state    = 0;
                break;
            case CMD_ARMED:
                system_state = STATE_ARMED;
                buzzer_paa   = 0;
                Buzzer_Off();
                PORTB = (PORTB & ~(1 << PB0)) | (1 << PB1);
                led_state = 0;
                break;
            case CMD_ALARM:
                system_state = STATE_ALARM;
                PORTB       |= (1 << PB1);
                buzzer_paa   = 1;
                Buzzer_On();
                break;
        }
    }

    /* Roed LED blinker hvert 250ms under alarm */
    if (system_state == STATE_ALARM && (uint16_t)(ms - last_blink) >= 250)
    {
        last_blink = ms;
        led_state ^= 1;
        if (led_state) PORTB |=  (1 << PB0);
        else           PORTB &= ~(1 << PB0);
    }
}

int main(void)
{
    DDRB  |=  (1 << PB0) | (1 << PB1);
    PORTB &= ~((1 << PB0) | (1 << PB1));

    Buzzer_Init();
    Buzzer_Off();

    /* Timer0 CTC 1ms: 1MHz / 8 / 125 = 1000 Hz */
    TCCR0  = (1 << WGM01) | (1 << CS01);
    OCR0   = 124;
    TIMSK |= (1 << OCIE0);

    I2C_Slave_Init(SLAVE2_ADDR);
    sei();

    set_sleep_mode(SLEEP_MODE_IDLE);

    while (1)
    {
        sleep_mode();
        }
        return 0;
}
