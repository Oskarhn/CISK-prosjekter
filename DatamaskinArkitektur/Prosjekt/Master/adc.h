/*
 * adc.h - ADC-bibliotek for master
 * ING1507 Datamaskinarkitektur
 * ATmega32 @ 1MHz
 *
 * Sensor: LM35 DFR0023 pa PA0 (ADC0)
 * Referanse: AVCC (5V)
 * Prescaler: 8 -> ADC-klokke = 125kHz (gyldig: 50-200kHz)
 *
 * LM35 formel:
 *   Vout = 10mV per grad Celsius
 *   ADC = (Vout / VREF) * 1024 = (Temp * 0.01 / 5.0) * 1024
 *   Temp = (ADC * 500) / 1024
 */
 
#ifndef ADC_H
#define ADC_H
 
#include <avr/io.h>
#include <stdint.h>
 
void ADC_Init(void)
{
    /* REFS1:0 = 01 -> AVCC som referanse */
    /* ADLAR   = 0  -> hoyre-justert      */
    /* MUX4:0  = 00000 -> ADC0 (PA0)      */
    ADMUX = (1 << REFS0);
 
    /* ADEN = 1 aktiver ADC                  */
    /* ADPS2:0 = 011 -> prescaler 8 (125kHz) */
    ADCSRA = (1 << ADEN) | (1 << ADPS1) | (1 << ADPS0);
}
 
uint16_t ADC_Read(uint8_t channel)
{
    /* Velg kanal, behold referanseinnstilling */
    ADMUX = (ADMUX & 0xE0) | (channel & 0x1F);
 
    ADCSRA |= (1 << ADSC);              /* Start konvertering */
    while (ADCSRA & (1 << ADSC));       /* Vent pa ferdig     */
 
    return ADC;  /* Les 10-bit resultat (ADCL+ADCH) */
}
 
/*
 * Leser temperatur fra LM35 pa ADC0.
 * Returnerer temperatur i hele grader Celsius.
 */
int16_t LM35_Read_Temp(void)
{
    uint16_t adc_val = ADC_Read(0); /* PA0 = ADC0 */
    /* Temp = (ADC * VREF * 100) / 1024
     *      = (ADC * 5000mV) / 1024 / 10mV
     *      = (ADC * 500) / 1024                */
    return (int16_t)((uint32_t)adc_val * 500UL / 1024UL);
}
 
#endif /* ADC_H */