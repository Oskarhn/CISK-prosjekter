/*
 * adc.h - ADC-bibliotek for slave 2
 * ING1507 Datamaskinarkitektur
 * ATmega32 @ 1MHz
 *
 * Sensor: LM35 DFR0023 pa PA0 (ADC0)
 * Referanse: AVCC (5V)
 * Prescaler: 8 -> ADC-klokke = 125kHz
 *
 * LM35 formel:
 *   Vout = 10mV per grad Celsius
 *   Temp(degC) = (ADC * 500) / 1024
 *
 * Eksempel: 25 grader -> Vout = 250mV
 *   ADC = (0.25 / 5.0) * 1024 = 51
 *   Temp = (51 * 500) / 1024 = 24.9 ~ 25 grader
 */
 
#ifndef ADC_H
#define ADC_H
 
#include <avr/io.h>
#include <stdint.h>
 
void ADC_Init(void)
{
    /* REFS1:0 = 01 -> AVCC referanse */
    /* MUX4:0  = 00000 -> ADC0 (PA0) */
    ADMUX  = (1 << REFS0);
 
    /* ADEN=1, prescaler 8 */
    ADCSRA = (1 << ADEN) | (1 << ADPS1) | (1 << ADPS0);
}
 
static uint16_t ADC_Read_Raw(void)
{
    /* Velg ADC0 (kanal 0) */
    ADMUX &= 0xE0;
 
    ADCSRA |= (1 << ADSC);         /* Start */
    while (ADCSRA & (1 << ADSC));  /* Vent  */
    return ADC;
}
 
/*
 * Leser LM35-temperatur.
 * Returnerer temperatur i hele grader Celsius (int16_t).
 */
int16_t LM35_Read_Temp(void)
{
    uint16_t raw = ADC_Read_Raw();
    return (int16_t)((uint32_t)raw * 500UL / 1024UL);
}
 
#endif /* ADC_H */