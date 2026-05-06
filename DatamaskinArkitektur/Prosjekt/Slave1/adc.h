/*
 * adc.h - ADC-bibliotek for slave 1
 * ING1507 Datamaskinarkitektur
 * ATmega32 @ 1MHz
 *
 * Sensor: Sharp GP2Y0A21 IR-avstandssensor pa PA1 (ADC1)
 * Referanse: AVCC (5V)
 * Prescaler: 8 -> ADC-klokke = 125kHz
 *
 * Sharp GP2Y0A21 karakteristikk:
 *   - Maleomrade: 10-80 cm
 *   - Hoy ADC-verdi = noe er naert (hoy utgspenning)
 *   - Lav ADC-verdi = ingenting i naerheten (lav spenning)
 *   - Spenning ved 10cm ca 2.3V -> ADC ca 471
 *   - Spenning ved 80cm ca 0.4V -> ADC ca 82
 *
 * IR_THRESHOLD: ADC-verdi over denne = noe detektert innenfor terskelavstand
 * Sett til 200 (tilsvarer ca 30cm). Juster etter testing.
 *
 * NB: Husk 10uF kondensator mellom VCC og GND pa sensoren.
 */
 
#ifndef ADC_H
#define ADC_H
 
#include <avr/io.h>
#include <stdint.h>
 
#define IR_THRESHOLD  200  /* ADC-verdi som tilsvarer ca 30cm. Juster etter testing. */
#define IR_CHANNEL      1  /* PA1 = ADC1, MUX4:0 = 00001 */
 
void ADC_Init(void)
{
    /* REFS1:0 = 01 -> AVCC som referanse */
    /* MUX4:0 = 00001 -> ADC1 (PA1)       */
    ADMUX  = (1 << REFS0) | (IR_CHANNEL & 0x1F);
 
    /* ADEN=1, prescaler 8 (ADPS1:ADPS0=1:1) */
    ADCSRA = (1 << ADEN) | (1 << ADPS1) | (1 << ADPS0);
}
 
uint16_t ADC_Read_IR(void)
{
    ADCSRA |= (1 << ADSC);         /* Start konvertering */
    while (ADCSRA & (1 << ADSC));  /* Vent pa ferdig     */
    return ADC;
}
 
/*
 * Returnerer 1 hvis noe detekteres innenfor terskelavstand.
 * Sensoren gir hoey spenning (hoy ADC) ved kort avstand.
 */
uint8_t IR_Detect(void)
{
    return (ADC_Read_IR() > IR_THRESHOLD) ? 1 : 0;
}
 
#endif /* ADC_H */