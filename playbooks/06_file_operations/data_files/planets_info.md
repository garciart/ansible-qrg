# Planet Information in Different Formats

-----

## Planet Information in CSV

```csv
name,diameter,hours_per_day,rings,largest_moon
Mercury,4879,4222.6,false,null
Venus,12104,2802.0,false,null
Earth,12756,24.0,false,Luna
Mars,6792,24.7,false,Phobos
Jupiter,142984,9.9,true,Ganymede
Saturn,120536,10.7,true,Titan
Uranus,51118,17.2,true,Titania
Neptune,49528,16.1,true,Triton
```

-----

## Planet Information in INI

```ini
; Planets Configuration File
; This is a list of the major planets.
title = "This is a list of the major planets."

[mercury]
diameter = 4879
hours_per_day = 4222.6
moons = null
name = "Mercury"
rings = false

[venus]
diameter = 12104
hours_per_day = 2802.0
moons = null
name = "Venus"
rings = false

[earth]
diameter = 12756
hours_per_day = 24.0
moons = "Luna"
name = "Earth"
rings = false

[mars]
diameter = 6792
hours_per_day = 24.7
moons = ["Phobos", "Deimos"]
name = "Mars"
rings = false

[jupiter]
diameter = 142984
hours_per_day = 9.9
moons = ["Ganymede", "Callisto", "Europa", "Io"],
name = "Jupiter"
rings = true

[saturn]
diameter = 120536
hours_per_day = 10.7
moons = ["Titan", "Rhea", "Iapetus", "Dione", "Tethys", "Enceladus", "Mimas"],
name = "Saturn"
rings = true

[uranus]
diameter = 51118
hours_per_day = 17.2
moons = ["Titania", "Oberon", "Umbriel", "Ariel", "Miranda"],
name = "Uranus"
rings = true

[neptune]
diameter = 49528
hours_per_day = 16.1
moons = "Triton"
name = "Neptune"
rings = true
```

-----

## Planet Information in XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<planets title="This is a list of the major planets.">
  <mercury>
    <name>Mercury</name>
    <diameter>4879</diameter>
    <hours_per_day>4222.6</hours_per_day>
    <rings>false</rings>
    <moons></moons>
  </mercury>
  <venus>
    <name>Venus</name>
    <diameter>12104</diameter>
    <hours_per_day>2802.0</hours_per_day>
    <rings>false</rings>
    <moons></moons>
  </venus>
  <earth>
    <name>Earth</name>
    <diameter>12756</diameter>
    <hours_per_day>24.0</hours_per_day>
    <rings>false</rings>
    <moons>
      <moon>Luna</moon>
    </moons>
  </earth>
  <mars>
    <name>Mars</name>
    <diameter>6792</diameter>
    <hours_per_day>24.7</hours_per_day>
    <rings>false</rings>
    <moons>
      <moon>Phobos</moon>
      <moon>Deimos</moon>
    </moons>
  </mars>
  <jupiter>
    <name>Jupiter</name>
    <diameter>142984</diameter>
    <hours_per_day>9.9</hours_per_day>
    <rings>true</rings>
    <moons>
      <moon>Ganymede</moon>
      <moon>Callisto</moon>
      <moon>Europa</moon>
      <moon>Io</moon>
    </moons>
  </jupiter>
  <saturn>
    <name>Saturn</name>
    <diameter>120536</diameter>
    <hours_per_day>10.7</hours_per_day>
    <rings>true</rings>
    <moons>
      <moon>Titan</moon>
      <moon>Rhea</moon>
      <moon>Iapetus</moon>
      <moon>Dione</moon>
      <moon>Tethys</moon>
      <moon>Enceladus</moon>
      <moon>Mimas</moon>
    </moons>
  </saturn>
  <uranus>
    <name>Uranus</name>
    <diameter>51118</diameter>
    <hours_per_day>17.2</hours_per_day>
    <rings>true</rings>
    <moons>
      <moon>Titania</moon>
      <moon>Oberon</moon>
      <moon>Umbriel</moon>
      <moon>Ariel</moon>
      <moon>Miranda</moon>
    </moons>
  </uranus>
  <neptune>
    <name>Neptune</name>
    <diameter>49528</diameter>
    <hours_per_day>16.1</hours_per_day>
    <rings>true</rings>
    <moons>
      <moon>Triton</moon>
    </moons>
  </neptune>
</planets>
```

## Planet Information in JSON

```json
{
    "planets": {
        "title": "This is a list of the major planets.",
        "mercury": {
            "diameter": 4879,
            "hours_per_day": 4222.6,
            "moons": null,
            "name": "Mercury",
            "rings": false
        },
        "venus": {
            "diameter": 12104,
            "hours_per_day": 2802.0,
            "moons": null,
            "name": "Venus",
            "rings": false
        },
        "earth": {
            "diameter": 12756,
            "hours_per_day": 24.0,
            "moons": "Luna",
            "name": "Earth",
            "rings": false
        },
        "mars": {
            "diameter": 6792,
            "hours_per_day": 24.7,
            "moons": [
                "Phobos",
                "Deimos"
            ],
            "name": "Mars",
            "rings": false
        },
        "jupiter": {
            "diameter": 142984,
            "hours_per_day": 9.9,
            "moons": [
                "Ganymede",
                "Callisto",
                "Europa",
                "Io"
            ],
            "name": "Jupiter",
            "rings": true
        },
        "saturn": {
            "diameter": 120536,
            "hours_per_day": 10.7,
            "moons": [
                "Titan",
                "Rhea",
                "Iapetus",
                "Dione",
                "Tethys",
                "Enceladus",
                "Mimas"
            ],
            "name": "Saturn",
            "rings": true
        },
        "uranus": {
            "diameter": 51118,
            "hours_per_day": 17.2,
            "moons": [
                "Titania",
                "Oberon",
                "Umbriel",
                "Ariel",
                "Miranda"
            ],
            "name": "Uranus",
            "rings": true
        },
        "neptune": {
            "diameter": 49528,
            "hours_per_day": 16.1,
            "moons": "Triton",
            "name": "Neptune",
            "rings": true
        }
    }
}
```

-----

## Planet Information in YAML

```yaml
---
planets:
  title: This is a list of the major planets.
  mercury:
    diameter: 4879
    hours_per_day: 4222.6
    moons: null
    name: Mercury
    rings: false
  venus:
    diameter: 12104
    hours_per_day: 2802.0
    moons: null
    name: Venus
    rings: false
  earth:
    diameter: 12756
    hours_per_day: 24.0
    moons:
      - Luna
    name: Earth
    rings: false
  mars:
    diameter: 6792
    hours_per_day: 24.7
    moons:
      - Phobos
      - Deimos
    name: Mars
    rings: false
  jupiter:
    diameter: 142984
    hours_per_day: 9.9
    moons:
      - Ganymede
      - Callisto
      - Europa
      - Io
    name: Jupiter
    rings: true
  saturn:
    diameter: 120536
    hours_per_day: 10.7
    moons:
      - Titan
      - Rhea
      - Iapetus
      - Dione
      - Tethys
      - Enceladus
      - Mimas
    name: Saturn
    rings: true
  uranus:
    diameter: 51118
    hours_per_day: 17.2
    moons:
      - Titania
      - Oberon
      - Umbriel
      - Ariel
      - Miranda
    name: Uranus
    rings: true
  neptune:
    diameter: 49528
    hours_per_day: 16.1
    moons:
      - Triton
    name: Neptune
    rings: true
...
```
