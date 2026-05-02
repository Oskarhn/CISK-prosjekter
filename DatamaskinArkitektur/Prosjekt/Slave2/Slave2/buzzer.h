/*
 * buzzer.h - Passiv buzzer, Timer1 CTC, toggle OC1A
 * ATmega32 @ 1MHz, PD5 (OC1A)
 *
 * Formel: f = f_CPU / (2 * N_ps * (ICR1 + 1)) = 62500 / (ICR1 + 1)
 *
 * Noteverdier (ICR1):
 *   D5 = 105  (~595 Hz)
 *   E5 =  93  (~665 Hz)
 *   G5 =  78  (~791 Hz)
 *   A5 =  70  (~880 Hz)
 *   0  = pause (lydlos)
 *
 * Meloditabell: { ICR1-verdi, lengde i 50 ms-tikk }
 * Stigende alarmmelodi: D5-E5-G5-A5-PAUSE, gjenta
 */

#ifndef BUZZER_H
#define BUZZER_H

#include <avr/io.h>
#include <stdint.h>

typedef struct { uint16_t icr; uint8_t len; } Note;

static const Note melody[] = {
    {105, 2},  /* D5  ~595 Hz   100 ms */
    { 93, 2},  /* E5  ~665 Hz   100 ms */
    { 78, 2},  /* G5  ~791 Hz   100 ms */
    { 70, 4},  /* A5  ~880 Hz   200 ms */
    {  0, 4},  /* Pause         200 ms */
};
#define MELODY_LEN ((uint8_t)(sizeof(melody) / sizeof(melody[0])))

static uint8_t mel_idx  = 0;
static uint8_t mel_tick = 0;

void Buzzer_Init(void)
{
    DDRD   |=  (1 << PD5);
    TCCR1A  = (1 << COM1A0);                          /* Toggle OC1A ved compare */
    TCCR1B  = (1 << WGM13) | (1 << WGM12) | (1 << CS11); /* CTC modus 12, prescaler 8 */
    ICR1    = melody[0].icr;
    TCCR1A &= ~(1 << COM1A0);                         /* Start stille */
    PORTD  &= ~(1 << PD5);
}

void Buzzer_On(void)
{
    mel_idx  = 0;
    mel_tick = 0;
    ICR1     = melody[0].icr;
    TCCR1A  |= (1 << COM1A0);   /* Koble OC1A til timer -> lyd */
}

void Buzzer_Off(void)
{
    TCCR1A &= ~(1 << COM1A0);   /* Koble fra OC1A -> stille */
    PORTD  &= ~(1 << PD5);
    mel_idx  = 0;
    mel_tick = 0;
}

/*
 * Buzzer_Melody_Update - Kalles fra Timer0 ISR hvert 50 ms.
 * Stegvis avspilling av meloditabellen.
 */
void Buzzer_Melody_Update(void)
{
    if (++mel_tick < melody[mel_idx].len)
        return;

    /* Gaa til neste note */
    mel_tick = 0;
    mel_idx  = (mel_idx + 1 >= MELODY_LEN) ? 0 : (mel_idx + 1);

    if (melody[mel_idx].icr == 0)
    {
        TCCR1A &= ~(1 << COM1A0); /* Pause: koble fra OC1A */
        PORTD  &= ~(1 << PD5);
    }
    else
    {
        ICR1    = melody[mel_idx].icr;
        TCCR1A |= (1 << COM1A0);  /* Note: koble til OC1A */
    }
}

#endif /* BUZZER_H */
