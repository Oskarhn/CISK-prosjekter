#define F_CPU 1000000UL
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
#include <stdint.h>
#include "i2c.h"

#define STATE_DISARMED  0
#define STATE_ARMED     1
#define STATE_ALARM     2

#define SERVO_LUKKET  188
#define SERVO_AAPEN   300
#define IR_TERSKEL    500

/* Delt mellom ISR-er */
volatile uint8_t  dor_apnet    = 0;
volatile uint8_t  ir_trigger   = 0;
volatile uint16_t dor_timer    = 0;
volatile uint16_t ir_cooldown  = 0;
volatile uint16_t ms           = 0;
volatile uint8_t  ir_armed     = 0;
volatile uint8_t  slave_status = STATUS_OK;

/* Sett av INT0 naar limit switch trykkes */
ISR(INT0_vect)
{
    if (!dor_timer) { dor_apnet = 1; dor_timer = 200; }
}

/* Sett av ADC naar maaling er ferdig */
ISR(ADC_vect)
{
    if (ADC > IR_TERSKEL) ir_trigger = 1;
}

ISR(TIMER0_COMP_vect)
{
    static uint8_t  ir_tick      = 0;
    static uint8_t  system_state = STATE_DISARMED;
    static uint8_t  rx_cmd       = 0;
    static uint8_t  led_state    = 0;
    static uint16_t last_blink   = 0;
    static uint16_t alarm_start  = 0;
    static uint8_t  in_alarm     = 0;

    ms++;
    if (dor_timer)   dor_timer--;
    if (ir_cooldown) ir_cooldown--;

    /* Start ADC-maaling hvert 40ms naar armert og ikke i cooldown */
    if (ir_armed && !ir_cooldown && ++ir_tick >= 40)
        { ir_tick = 0; ADCSRA |= (1 << ADSC); }

    /* ta imot kommando fra master */
    if (I2C_Slave_Poll(&rx_cmd, slave_status) == 1)
    {
        switch (rx_cmd)
        {
            case CMD_DISARMED:
                system_state = STATE_DISARMED;
                slave_status = STATUS_OK;
                ir_armed     = 0;
                dor_apnet    = 0;
                ir_trigger   = 0;
                ir_cooldown  = 0;
                in_alarm     = 0;
                OCR1A        = SERVO_LUKKET;
                PORTB       &= ~(1 << PB0);
                led_state    = 0;
                break;
            case CMD_ARMED:
                system_state = STATE_ARMED;
                slave_status = STATUS_OK;
                ir_armed     = 1;
                break;
            case CMD_ALARM:
                system_state = STATE_ALARM;
                ir_armed     = 1;
                break;
        }
    }

    /* Alarmvurdering */
    uint8_t local_alarm = (dor_apnet || ir_trigger) && (system_state != STATE_DISARMED);
    uint8_t show_alarm  = local_alarm || (system_state == STATE_ALARM);

    if (local_alarm)
    {
        slave_status = STATUS_DOOR_OPEN;
        if (!in_alarm) { in_alarm = 1; alarm_start = ms; }
    }

    if (show_alarm)
    {
        OCR1A = SERVO_AAPEN;

        uint16_t halvperiode = (local_alarm && dor_apnet) ? 250 : 62;
        if ((uint16_t)(ms - last_blink) >= halvperiode)
        {
            last_blink = ms;
            led_state ^= 1;
            if (led_state) PORTB |=  (1 << PB0);
            else           PORTB &= ~(1 << PB0);
        }

        /* Auto-reset etter 5 sek */
        if (local_alarm && (uint16_t)(ms - alarm_start) >= 5000)
        {
            dor_apnet    = 0;
            ir_trigger   = 0;
            ir_cooldown  = 2000;
            slave_status = STATUS_OK;
            in_alarm     = 0;
        }
    }
    else
    {
        OCR1A     = SERVO_LUKKET;
        PORTB    &= ~(1 << PB0);
        led_state  = 0;
        in_alarm   = 0;
    }
}

int main(void)
{
    DDRB  |=  (1 << PB0);
    PORTB &= ~(1 << PB0);

    DDRD  &= ~(1 << PD2);
    PORTD |=  (1 << PD2);
    MCUCR |= (1 << ISC01) | (1 << ISC00);
    GICR  |= (1 << INT0);

    ADMUX  = (1 << REFS0) | 1;
    ADCSRA = (1 << ADEN) | (1 << ADIE) | (1 << ADPS1) | (1 << ADPS0);

    /* Servo: Timer1 Fast PWM, prescaler 8, ICR1=2499 -> 20ms */
    DDRD  |=  (1 << PD5);
    TCCR1A = (1 << COM1A1) | (1 << WGM11);
    TCCR1B = (1 << WGM13)  | (1 << WGM12) | (1 << CS11);
    ICR1   = 2499;
    OCR1A  = SERVO_LUKKET;

    TCCR0  = (1 << WGM01) | (1 << CS01);
    OCR0   = 124;
    TIMSK |= (1 << OCIE0);

    I2C_Slave_Init(SLAVE1_ADDR);
    sei();

    set_sleep_mode(SLEEP_MODE_IDLE);

    while (1)
    {
        sleep_mode();
        }
        return 0;
}