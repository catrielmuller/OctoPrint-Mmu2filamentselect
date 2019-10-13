---
layout: plugin

id: mmufilamentselect
title: octoprint-mmufilamentselect
description: Select the filament for Prusa MMU when printing in single mode.
author: Florian Schütte
license: AGPLv3

date: 2019-10-04

homepage: https://github.com/derPicknicker1/OctoPrint-Mmu2filamentselect
source: https://github.com/derPicknicker1/OctoPrint-Mmu2filamentselect
archive: https://github.com/derPicknicker1/OctoPrint-Mmu2filamentselect/archive/master.zip

follow_dependency_links: false

tags:
- prusa
- mmu
- mmu1
- mmu2
- gcode
- prusa mmu2
- prusa mmu1
- single
- color
- filament
- notification

screenshots:
- url: /assets/img/plugins/mmu2filamentselect/dialog.png
  alt: Picture of the filament selection dialog.
  caption: Dialog which is shown when filament has to be selected.
- url: /assets/img/plugins/mmu2filamentselect/settings2.png
  alt: Picture of the settings dialog.
  caption: The dialog timeout can be set by the user.


featuredimage: /assets/img/plugins/mmu2filamentselect/octoprusa.png

---

<img src="https://plugins.octoprint.org/assets/img/plugins/mmu2filamentselect/octoprusa.png" width="25%" align="left"> 

This plugin shows a dialog to select the filament when a print on a Prusa printer with MMU2 is startet in single mode.

The dialog is shown, when the plugin detects a 'Tx' command in the gcode.

So you don't have to go to your printer and select the filament to be used. It can now be done from within Octoprint.

A timeout can be set in the settings (default 30 seconds), after which the dialog is closed. When this happens you have to select the filament on the printer as usual.
