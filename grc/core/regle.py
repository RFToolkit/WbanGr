# Table 11: Table of event codes. The most recent version of this table will be available from [1]
# http://biosig.svn.sourceforge.net/viewvc/biosig/trunk/biosig/doc/eventcodes.txt
### Table of event codes.
# This file is part of the biosig project http://biosig.sf.net/
# Copyright (C) 2004 Alois Schloegl <a.schloegl@ieee.org>
# $Id: eventcodes.txt,v 1.3 2004/06/17 17:08:54 schloegl Exp $
### table of event codes: lines starting with # are omitted
### add 0x8000 to indicate end of event
#
REGLE={
    "010": "EEG artifacts",
    "0101": "artifact:EOG",
    "0102": "artifact:ECG",
    "0103": "artifact:EMG/Muscle",
    "0104": "artifact:Movement",
    "0105": "artifact:Failing Electrode",
    "0106": "artifact:Sweat",
    "0107": "artifact:50/60 Hz mains interference",
    "0108": "artifact:breathing",
    "0109": "artifact:pulse",
    "011": "EEG patterns",
    "0111": "eeg:Sleep spindles",
    "0112": "eeg:K-complexes",
    "0113": "eeg:Saw-tooth waves",
    "003": "Trigger, cues, classlabels",
    "0300": "Trigger, start of Trial (unspecific)",
    "0301": "Left - cue onset (BCI experiment)",
    "0302": "Right - cue onset (BCI experiment)",
    "0303": "Foot - cue onset (BCI experiment)",
    "0304": "Tongue - cue onset (BCI experiment)",
    "0306": "Down - cue onset (BCI experiment)",
    "030C": "Up - cue onset (BCI experiment)",
    "030D": "Feedback (continuous) - onset (BCI experiment)",
    "030E": "Feedback (discrete) - onset (BCI experiment)",
    "0311": "Beep (accustic stimulus, BCI experiment)",
    "0312": "Cross on screen (BCI experiment)",
    "03ff": "Rejection of whole trial",
    "040": "Sleep-related Respiratory Events",
    "0401": "Obstructive Apnea/Hypopnea Event (OAHE)",
    "0402": "Respiratory Effort Related Arousal (RERA)",
    "0403": "Central Apnea/Hypopnea Event (CAHE)",
    "0404": "Cheyne-Stokes Breathing (CSB)",
    "0405": "Sleep Hypoventilation",
    "041": "Sleep stages according to Rechtschaffen&Kales",
    "0410": "Wake",
    "0411": "Stage 1",
    "0412": "Stage 2",
    "0413": "Stage 3",
    "0414": "Stage 4",
    "0415": "REM",
    "050": "ECG events",
    "0501": "ecg:Fiducial point of QRS complex",
    "0502": "ecg:P-wave",
    "0503": "ecg:Q-point",
    "0504": "ecg:R-point",
    "0505": "ecg:S-point",
    "0506": "ecg:T-point",
    "0507": "ecg:U-wave",
    "0000": "OTHER: No event",
    "7FFF": "OTHER: non-equidistant sampled value"
}