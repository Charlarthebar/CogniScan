# Cognitive Assessment Tool

A comprehensive cognitive screening application built with Python and Kivy, designed to evaluate multiple domains of cognitive function through standardized neuropsychological tests.

## Important Disclaimer

**This application is NOT a medical diagnostic tool.**

This software is designed for educational and research purposes only. It cannot diagnose dementia, Alzheimer's disease, or any other medical condition. Results from this screening should be interpreted by qualified healthcare professionals as part of a comprehensive clinical evaluation.

If you have concerns about cognitive health, please consult a physician, neurologist, or neuropsychologist for proper assessment.

## Overview

This cognitive assessment tool evaluates seven key cognitive domains based on elements from established neuropsychological assessments including the Mini-Mental State Examination (MMSE) and Montreal Cognitive Assessment (MoCA):

| Test | Domain | Points | Description |
|------|--------|--------|-------------|
| Orientation | Temporal awareness | 5 | Questions about current date, day, month, year, and season |
| Immediate Recall | Short-term memory | 5 | Memorize and immediately recall 5 words |
| Serial 7s | Attention & calculation | 5 | Subtract 7 from 100 repeatedly (5 subtractions) |
| Digit Span | Working memory | 4 | Repeat digits forward and backward |
| Category Fluency | Verbal fluency | 3 | Name as many animals as possible in 60 seconds |
| Stroop Test | Executive function | 5 | Identify ink color while ignoring word meaning |
| Delayed Recall | Long-term memory | 5 | Recall the 5 words from earlier in the test |

**Total Score: 30 points** (normalized from 32 raw points)

## Score Interpretation

| Score Range | Category | Description |
|-------------|----------|-------------|
| 26-30 | Normal Cognition | Cognitive functions performing as expected |
| 18-25 | Mild Cognitive Impairment | Possible MCI; recommend clinical evaluation |
| 10-17 | Moderate Cognitive Impairment | Significant difficulties; seek medical evaluation |
| 0-9 | Severe Cognitive Impairment | Substantial impact on daily activities |

**Note:** These ranges are approximations based on research literature and should not be used for self-diagnosis.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/CharlesJLai/Dementia-Diagnosis.git
cd Dementia-Diagnosis
```

2. (Recommended) Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### Assessment Flow

1. **Introduction** - Read the disclaimer and understand the assessment
2. **Orientation (Phase 1)** - Answer 5 questions about the current date
3. **Word Memorization (Phase 2)** - View and memorize 5 words (10 seconds)
4. **Immediate Recall** - Enter the words you remember
5. **Serial 7s (Phase 3)** - Count down from 100 by 7s
6. **Digit Span (Phase 4)** - Repeat number sequences forward and backward
7. **Category Fluency (Phase 5)** - Name animals for 60 seconds
8. **Stroop Test (Phase 6)** - Identify ink colors (10 trials, 30 seconds)
9. **Delayed Recall (Phase 7)** - Recall the 5 words from Phase 2
10. **Results** - View your comprehensive score and interpretation

### Tips for Best Results

- Complete the assessment in a quiet environment
- Ensure you are well-rested and not under the influence of medications that may affect cognition
- Read all instructions carefully before each test
- The assessment takes approximately 15-20 minutes

## Project Structure

```
Dementia-Diagnosis/
├── main.py                 # Application logic and test implementations
├── dementiadiagnosis.kv    # Kivy UI layout and styling
├── words.txt               # Word bank for memory tests
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Technical Details

### Technologies Used

- **Python 3.8+** - Core programming language
- **Kivy 2.2+** - Cross-platform UI framework
- **Kivy Properties** - Reactive data binding for UI updates

### Cognitive Tests Based On

The tests in this application are adapted from established neuropsychological assessments:

- **Mini-Mental State Examination (MMSE)** - Folstein et al., 1975
- **Montreal Cognitive Assessment (MoCA)** - Nasreddine et al., 2005
- **Stroop Color and Word Test** - Stroop, 1935
- **Digit Span** - Wechsler Memory Scale

### Scoring Methodology

- Raw scores are collected from each test (total 32 points)
- Scores are normalized to a 30-point scale for interpretation
- Category cutoffs are based on MoCA normative data
- Scoring accounts for common variants in established tests

## Limitations

1. **Not a Diagnostic Tool** - This screening cannot replace professional clinical evaluation
2. **Environmental Factors** - Results may be affected by fatigue, stress, distractions, or technical issues
3. **Practice Effects** - Repeated use may lead to improved scores unrelated to cognitive function
4. **Population Variance** - Normative data may not apply equally to all populations
5. **Self-Administration** - Lacks the clinical observation component of professional assessments
6. **Language/Culture** - Designed for English speakers; may not be culturally appropriate for all users

## Privacy & Data

- This application does not collect, store, or transmit any user data
- All assessment data exists only during the active session
- No personally identifiable information is required or stored
- Results are displayed only on-screen and are not saved

## Research References

1. Folstein, M. F., Folstein, S. E., & McHugh, P. R. (1975). "Mini-mental state": A practical method for grading the cognitive state of patients for the clinician. *Journal of Psychiatric Research*, 12(3), 189-198.

2. Nasreddine, Z. S., et al. (2005). The Montreal Cognitive Assessment, MoCA: A brief screening tool for mild cognitive impairment. *Journal of the American Geriatrics Society*, 53(4), 695-699.

3. Stroop, J. R. (1935). Studies of interference in serial verbal reactions. *Journal of Experimental Psychology*, 18(6), 643-662.

4. Wechsler, D. (2008). *Wechsler Adult Intelligence Scale–Fourth Edition (WAIS-IV)*. San Antonio, TX: Pearson.

## Contributing

Contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

Please ensure any contributions maintain the educational and non-diagnostic nature of this tool.

## License

This project is provided for educational and research purposes. Please ensure appropriate ethical review and informed consent procedures if using in research contexts.

## Acknowledgments

- Inspired by established neuropsychological assessment tools
- Built with the Kivy framework
- Developed as an educational project to understand cognitive screening methodologies
