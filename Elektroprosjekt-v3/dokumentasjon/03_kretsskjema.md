# 03. Kontrollkrets — V3-HIGHPOWER

## Oversikt

Styrer lading og trigger av Marx-generator.

## Viktig begrensning

Reed relay DAT70510-HR er rated til 7.5kV.
Marx utgang er 8kV. 

**Løsning:** Bruk **to relay i serie** (15kV total) 
ELLER aksepter 0.5kV overskridelse (risiko).

## Blokkskjema

[Arduino] → [Driver] → [Reed Relay A] → [Reed Relay B] → [Trigger]
↓
[Marx 10-steg]
↓
[Peaking] → [TEM]

## Komponenter

### 1. Arduino Nano
- Styrer ladingstid (0.75s), trigger, sikkerhet

### 2. Driver
- Transistor: 2N2222 eller MOSFET
- Last: To reed relay spoler (56Ω total)

### 3. Reed Reléer (TO I SERIE!)
- **Type:** Cynergy3 DAT70510-HR (2 stk)
- **Farnell:** [2663956](https://no.farnell.com/cynergy3/dat70510-hr/reed-relay-spst-no-7kv-2a-th/dp/2663956)
- **Total rating:** 15kV (sikkert for 8kV)

### 4. Sikkerhetsinterlock
- NC nødstopp-knapp (tangen)
- Dør-switch (kabinett)
- "Ladet" LED (rød, via spenningsdeler)
- "Klar" LED (grønn)

## Kretsdiagram

+5V
      │
     1kΩ
      │

D2 ───────┤──┬──→ Relay A spole (28Ω)
│ │
│ ├──→ Relay B spole (28Ω)
│ │
GND │
│
[DAT70510-HR] × 2 (i serie)
│
HV+ (2.4kV) → Trigger Marx

## Program (Arduino)

```cpp
const int TRIGGER = 2;
const int CHARGE = 3;
const int LED_READY = 4;
const int LED_CHARGED = 5;
const int INTERLOCK = 6;  // Dør + nødstopp

void setup() {
  pinMode(TRIGGER, OUTPUT);
  pinMode(CHARGE, OUTPUT);
  pinMode(LED_READY, OUTPUT);
  pinMode(LED_CHARGED, OUTPUT);
  pinMode(INTERLOCK, INPUT_PULLUP);
  
  digitalWrite(TRIGGER, LOW);
  digitalWrite(CHARGE, LOW);
  Serial.begin(9600);
  Serial.println("V3-HIGHPOWER Kontrollsystem");
  Serial.println("ADVARSEL: 8000V system");
}

void loop() {
  // Sjekk interlock (må være HIGH = lukket)
  if (digitalRead(INTERLOCK) == LOW) {
    Serial.println("FEIL: Interlock åpen!");
    delay(1000);
    return;
  }
  
  digitalWrite(LED_READY, HIGH);
  Serial.println("Lader...");
  
  // Lading
  digitalWrite(CHARGE, HIGH);
  delay(750);  // 0.75s (5τ)
  digitalWrite(CHARGE, LOW);
  
  digitalWrite(LED_READY, LOW);
  digitalWrite(LED_CHARGED, HIGH);
  Serial.println("LADET! Klar til ildgivning.");
  
  delay(500);  // Stabilisering
  
  // FIRE!
  Serial.println("FIRING!");
  digitalWrite(TRIGGER, HIGH);
  delay(20);   // 20ms trigger
  digitalWrite(TRIGGER, LOW);
  
  digitalWrite(LED_CHARGED, LOW);
  Serial.println("Puls fullført. Cooldown...");
  delay(2000);  // 2s cooldown
}

// Nødstopp: Trykk reset-knapp på Arduino

Sikkerhetskrav

    To relay i serie ELLER akseptert risiko
    Interlock på kabinettdør (NC)
    Nødstopp-knapp (tangen)
    "Ladet" indikator (rød LED)
    Fjernstyrt triggering (>5m)
    15kV isolasjon mellom lavspenning og Marx

Måling av "Ladet" status

Bruk spenningsdeler 1000:1 (10MΩ + 10kΩ) til Arduino A0.
ADVARSEL: Spenningsdeler må tåle 8kV!