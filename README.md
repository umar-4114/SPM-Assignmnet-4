# SPM Assignment 04
## Optimizing Agile Software Delivery: Simulation and Risk Mitigation for a Multi-Team Project

**Course:** Software Project Management  
**Instructor:** Ms. Isra Zafat  
**Section:** BS SE (Red + Green) F22  
**Semester:** Fall 2025

---

## 📋 Project Overview

This repository contains a comprehensive Monte Carlo simulation for optimizing Agile software delivery in a multi-team environment. The project models a realistic scenario with:

- **210 user stories** (1,657 story points)
- **3 cross-functional teams** with varying capabilities
- **8 identified risks** with quantified probabilities and impacts
- **1,000 Monte Carlo simulations** for statistical analysis
- **Technical debt modeling** and accumulation
- **Resource contention** and velocity modeling
- **Earned Value Management** (EVM) analysis

### Key Features

✅ **Data-Driven Planning:** Realistic backlog, team configurations, and risk register  
✅ **Monte Carlo Simulation:** 1,000 iterations with confidence intervals  
✅ **Comprehensive Visualizations:** 9 professional charts and graphs  
✅ **Sensitivity Analysis:** Tornado charts identifying key impact factors  
✅ **Risk Mitigation Strategies:** Quantified ROI on mitigation investments  
✅ **Detailed Reporting:** 50+ page comprehensive report with EVM analysis  

---

## 📁 Repository Structure

```
├── README.md                    # This file - complete instructions
├── requirements.txt             # Python dependencies
├── REPORT.md                    # Comprehensive 50+ page project report
├── status_report.md            # Mid-project status report
├── simulation.ipynb            # Jupyter notebook (basic structure)
├── run_simulation.py           # Complete simulation script
├── data/
│   ├── backlog.csv            # 210 user stories with dependencies
│   ├── teams.json             # 3 team configurations
│   └── risks.json             # 8 risk definitions
└── output/
    ├── backlog_analysis.png           # Backlog composition analysis
    ├── velocity_distributions.png     # Team velocity distributions
    ├── monte_carlo_completion.png     # Project completion histogram
    ├── monte_carlo_cost.png           # Project cost histogram
    ├── burndown_chart.png             # Burndown with scope change
    ├── velocity_trend.png             # Sprint velocity over time
    ├── earned_value.png               # EVM analysis (PV, EV, AC)
    ├── risk_impact.png                # Risk occurrence frequency
    ├── sensitivity_tornado.png        # Sensitivity analysis
    ├── simulation_results.pkl         # Raw simulation data
    └── simulation_summary.csv         # Summary statistics
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/umar-4114/SPM-Assignment-04.git
cd SPM-Assignment-04
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

Required packages:
- `numpy>=1.24.0` - Numerical computing
- `pandas>=2.0.0` - Data manipulation
- `matplotlib>=3.7.0` - Plotting
- `seaborn>=0.12.0` - Statistical visualizations
- `scipy>=1.10.0` - Scientific computing

### Running the Simulation

**Option 1: Run the complete simulation script**
```bash
python run_simulation.py
```

This will:
- Load all project data
- Run 1,000 Monte Carlo simulations
- Generate all 9 visualizations
- Save results to `output/` directory
- Display progress and summary statistics

**Execution time:** ~3-5 minutes on modern hardware

**Option 2: Use Jupyter Notebook (Interactive)**
```bash
jupyter notebook simulation.ipynb
```

Or with JupyterLab:
```bash
jupyter lab simulation.ipynb
```

---

## 📊 Understanding the Outputs

### 1. Backlog Analysis (`backlog_analysis.png`)

**What it shows:**
- Story point distribution (histogram)
- Complexity breakdown (Small/Medium/Large)
- Priority distribution (High/Medium/Low pie chart)
- Technical debt factor distribution

**Key insights:**
- 71% of stories are Medium complexity (5-8 SP)
- High priority work = 44.2% of backlog
- Average technical debt factor = 14.71%

### 2. Velocity Distributions (`velocity_distributions.png`)

**What it shows:**
- Probability distribution of each team's velocity
- Normal distribution curves for 3 teams
- Expected velocity (red line) vs simulated range

**Key insights:**
- Team Alpha: 45 ± 6 SP/sprint (highest capacity)
- Team Beta: 38 ± 5 SP/sprint (balanced)
- Team Gamma: 32 ± 4 SP/sprint (frontend focus)

### 3. Monte Carlo Completion (`monte_carlo_completion.png`)

**What it shows:**
- Distribution of project completion times (left)
- Distribution of project costs (right)
- Mean, median, and baseline estimates

**Key findings:**
- Mean completion: **34.2 sprints** (vs 15 baseline)
- Mean cost: **$3,010,091** (vs $1,905,000 baseline)
- 95% confidence: 28-41 sprints

### 4. Monte Carlo Cost (`monte_carlo_cost.png`)

**What it shows:**
- Detailed cost distribution histogram
- Cost statistics and variance

**Key findings:**
- 58% cost overrun from baseline
- Standard deviation: $438,335
- Budget recommendation: $3.2M with 20% contingency

### 5. Burndown Chart (`burndown_chart.png`)

**What it shows:**
- Actual progress (blue line)
- Ideal burndown (green line)
- Baseline ideal (orange line)
- Scope change event (red vertical line at Sprint 5)

**Key insights:**
- Scope increase of 58 SP at Sprint 5
- Velocity decline visible after Sprint 12
- Realistic S-curve progression

### 6. Velocity Trend (`velocity_trend.png`)

**What it shows:**
- Sprint-by-sprint velocity (bars)
- 3-sprint moving average (red line)
- Expected velocity (green line)

**Key insights:**
- Initial velocity: 118 SP/sprint (above target)
- Mid-project: 105 SP/sprint (stabilized)
- Late project: 88 SP/sprint (technical debt impact)

### 7. Earned Value Management (`earned_value.png`)

**What it shows:**
- Planned Value (PV) - blue line
- Earned Value (EV) - green line
- Actual Cost (AC) - red line (secondary axis)
- CPI and SPI indices

**Key metrics:**
- CPI = 0.94 (6% over budget)
- SPI = 1.02 (2% ahead of schedule)
- EAC = $4,562,000 (projected final cost)

### 8. Risk Impact (`risk_impact.png`)

**What it shows:**
- Risk occurrence frequency (left)
- Risk probability profile (right)

**Top risks:**
1. Scope Creep (99.7% of simulations)
2. Technical Debt Accumulation (93.2%)
3. Integration Issues (83.1%)

### 9. Sensitivity Tornado (`sensitivity_tornado.png`)

**What it shows:**
- Impact of ±20% parameter variation
- Most impactful factors at top

**Key finding:**
- **Team velocity** has 40x more impact than velocity standard deviation
- Focus optimization on increasing mean velocity, not reducing variance

---

## 📖 Documentation

### Main Report (`REPORT.md`)

Comprehensive 50+ page report including:

1. **Executive Summary** - Key findings and recommendations
2. **Introduction** - Project context and objectives
3. **Initial Planning** - Backlog analysis and team allocation
4. **Simulation Model** - Technical methodology and formulas
5. **Quantitative Results** - Monte Carlo analysis with confidence intervals
6. **Mid-Project Status** - Burndown, velocity trends, EVM
7. **Risk Analysis** - Identified risks and mitigation strategies
8. **Recommendations** - Data-driven optimization strategies
9. **Conclusion** - Key takeaways and success metrics
10. **Appendix** - Formulas, parameters, and references

### Status Report (`status_report.md`)

Mid-project status report (Sprint 17) including:

- Sprint-by-sprint progress tracking
- Team performance analysis
- Burndown and velocity trends
- EVM metrics (CPI, SPI, EAC, ETC)
- Active risks and issues
- Technical debt status
- Corrective actions
- Stakeholder communication summary
- Key decisions required

---

## 🔬 Methodology

### Monte Carlo Simulation Process

```python
For each of 1,000 iterations:
    1. Initialize project state
    2. While work remains and sprints < 50:
        a. Apply scope changes (if applicable)
        b. For each team:
            - Calculate base velocity ~ N(μ, σ)
            - Apply technical debt factor
            - Check resource contention
            - Check risk occurrences
            - Apply risk impacts
        c. Complete story points
        d. Update costs
        e. Track metrics
    3. Record results (sprints, cost, risks)
```

### Key Formulas

**Effective Velocity:**
```
effective_velocity = base_velocity × (1 - technical_debt) × (1 - contention_factor)
```

**Technical Debt Accumulation:**
```
debt(t) = debt(0) × (1 + 0.02 × t)
debt(t) = min(debt(t), 0.30)  # Capped at 30%
```

**Earned Value Metrics:**
```
CPI = EV / AC
SPI = EV / PV
EAC = AC / CPI
ETC = EAC - AC
```

---

## 🎯 Key Findings

### Project Completion

| Metric | Baseline | Simulated | Variance |
|--------|----------|-----------|----------|
| **Sprints** | 15 | 34.2 | +127% |
| **Duration** | 30 weeks | 68.4 weeks | +128% |
| **Cost** | $1,905,000 | $3,010,091 | +58% |

### Confidence Intervals

**Sprints to Completion:**
- 50% CI: 32-36 sprints
- 80% CI: 30-39 sprints
- 95% CI: 28-41 sprints

**Project Cost:**
- 50% CI: $2.8M - $3.2M
- 80% CI: $2.5M - $3.5M
- 95% CI: $2.5M - $3.6M

### Sensitivity Analysis

**Impact of ±20% parameter variation:**

| Parameter | Impact (Sprints) | % Change |
|-----------|------------------|----------|
| Team Velocity | ±13.79 | ±40.3% |
| Velocity Std Dev | ±0.22 | ±0.6% |

**Key insight:** Team velocity is the **single most impactful factor** (40% impact)

### Risk Analysis

**Most Frequent Risks:**
1. Scope Creep (30% probability, 99.7% occurrence)
2. Technical Debt (28% probability, 93.2% occurrence)
3. Integration Issues (25% probability, 83.1% occurrence)

**Average risk events per simulation:** 105.34 (3.08 per sprint)

---

## 💡 Recommendations

### 1. Optimize Team Velocity (+12-15% improvement)

**Investment:** $150,000
- Technical training: $75,000
- Remove impediments: $50,000
- Process optimization: $25,000

**Expected Impact:**
- Sprint reduction: 5-6 sprints
- Cost savings: $711,200
- **ROI: 4.7x**

### 2. Manage Technical Debt (Reduce from 14.71% to 8%)

**Investment:** $802,000
- 6 hardening sprints: $762,000
- Quality tools: $40,000

**Expected Impact:**
- Prevent velocity degradation
- Sprint reduction: 3-4 sprints
- **ROI: 0.5-0.6x** (necessary for viability)

### 3. Proactive Risk Management (-25% risk occurrence)

**Investment:** $200,000
- Risk manager: $120,000
- Tools and processes: $80,000

**Expected Impact:**
- Sprint reduction: 2-3 sprints
- Cost savings: $254,000 - $381,000
- **ROI: 1.3-1.9x**

### Combined Optimization

**Total Investment:** $1,152,000  
**Expected Results:**
- Duration: 28.9 sprints (vs 34.2 baseline) = **-15.5%**
- Cost: $2,368,300 (vs $3,010,091 baseline) = **-21.3%**
- **ROI: 1.4x** (including time-to-market value)

---

## 🔧 Customization

### Modifying Simulation Parameters

Edit `run_simulation.py` or the notebook:

```python
SIMULATION_CONFIG = {
    'num_simulations': 1000,        # Number of Monte Carlo iterations
    'sprint_duration_weeks': 2,     # Sprint length
    'scope_change_sprint': 5,       # When scope change occurs
    'scope_change_points': 58,      # Additional story points
    'technical_debt_accumulation_rate': 0.02,  # 2% per sprint
    'resource_contention_probability': 0.25,   # 25% chance per sprint
    'resource_contention_impact': 0.10,        # 10% velocity reduction
}
```

### Updating Team Configurations

Edit `data/teams.json`:

```json
{
  "teams": [
    {
      "team_id": "ALPHA",
      "team_name": "Team Alpha",
      "average_velocity": 45,    // Adjust velocity
      "velocity_std": 6,          // Adjust variance
      "cost_per_sprint": 50000,   // Adjust cost
      "specialization": "Backend and API development"
    }
  ]
}
```

### Adding New Risks

Edit `data/risks.json`:

```json
{
  "risk_id": "R009",
  "risk_name": "Your Risk Name",
  "description": "Risk description",
  "probability": 0.20,           // 20% chance
  "impact_type": "velocity_reduction",  // or "cost_increase", "delay"
  "impact_value": 0.15,          // 15% reduction
  "duration_sprints": 2          // Lasts 2 sprints
}
```

### Modifying Backlog

Edit `data/backlog.csv`:

```csv
Story ID,Story Name,Story Points,Complexity,Technical Debt Factor,Dependencies,Priority
US999,New Story,8,Medium,0.12,US001|US002,High
```

---

## 📚 Technical Details

### Dependencies Explained

- **NumPy:** Numerical operations, random number generation, statistical functions
- **Pandas:** Data loading, manipulation, analysis of backlog and results
- **Matplotlib:** Base plotting library for all visualizations
- **Seaborn:** Statistical plotting (distributions, heatmaps)
- **SciPy:** Advanced statistical functions (not heavily used but available)

### Performance Considerations

- **1,000 simulations:** ~3-5 minutes
- **10,000 simulations:** ~30-40 minutes (for higher precision)
- **Memory usage:** ~200MB (results stored in memory)
- **Output size:** ~7MB (mostly visualization PNGs)

### Random Seed

The simulation uses `np.random.seed(42)` for reproducibility. To get different random results:

```python
np.random.seed(None)  # Use system time
# or
np.random.seed(123)   # Use different seed
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'numpy'`  
**Solution:** Install dependencies: `pip install -r requirements.txt`

**Issue:** Simulation runs but no visualizations appear  
**Solution:** Check that `output/` directory exists. Script creates it automatically but check permissions.

**Issue:** "RuntimeWarning: invalid value encountered"  
**Solution:** This is normal - occurs when velocity calculations hit edge cases. Results are still valid.

**Issue:** Jupyter notebook kernel crashes  
**Solution:** Reduce `num_simulations` from 1000 to 100 for testing, or increase available memory.

**Issue:** Plots don't show in Jupyter  
**Solution:** Add `%matplotlib inline` at the top of the notebook.

### Getting Help

For issues or questions:
1. Check existing documentation in REPORT.md
2. Review code comments in run_simulation.py
3. Open an issue on GitHub repository

---

## 📈 Extending the Project

### Possible Enhancements

1. **Machine Learning Integration:**
   - Train predictive models on historical project data
   - Anomaly detection for early warning

2. **Interactive Dashboard:**
   - Build Streamlit or Dash web interface
   - Real-time parameter adjustment

3. **Multi-Objective Optimization:**
   - Pareto frontier analysis
   - Trade-off curves (time vs cost vs quality)

4. **Dependency Network Analysis:**
   - Graph visualization of story dependencies
   - Critical path algorithms

5. **Team Dynamics Modeling:**
   - Tuckman's stages (forming, storming, norming, performing)
   - Morale and burnout prediction

---

## 📝 Assignment Checklist

### Data Files ✅
- [x] `data/backlog.csv` - 210+ user stories
- [x] `data/teams.json` - 3 team configurations
- [x] `data/risks.json` - 8+ risks with probabilities

### Simulation Code ✅
- [x] Section 1: Project Planning and Setup
- [x] Section 2: Velocity and Technical Debt Modeling
- [x] Section 3: Risk and Scope Management
- [x] Section 4: Monte Carlo Simulation (1000+ runs)
- [x] Section 5: Sensitivity Analysis

### Visualizations (9 PNG files) ✅
- [x] `output/backlog_analysis.png`
- [x] `output/velocity_distributions.png`
- [x] `output/monte_carlo_completion.png`
- [x] `output/monte_carlo_cost.png`
- [x] `output/burndown_chart.png`
- [x] `output/velocity_trend.png`
- [x] `output/earned_value.png`
- [x] `output/risk_impact.png`
- [x] `output/sensitivity_tornado.png`

### Documentation ✅
- [x] `REPORT.md` - Comprehensive 50+ page report
- [x] `status_report.md` - Mid-project status
- [x] `README.md` - Complete instructions (this file)
- [x] `requirements.txt` - Python dependencies

### Code Quality ✅
- [x] Well-commented code
- [x] Modular functions
- [x] Clear variable naming
- [x] Reproducible results (random seed)

---

## 🏆 Learning Outcomes

This project demonstrates proficiency in:

1. **Quantitative Analysis:**
   - Monte Carlo simulation
   - Statistical analysis (confidence intervals)
   - Probability distributions

2. **Agile Project Management:**
   - Sprint planning and estimation
   - Velocity tracking
   - Backlog management

3. **Risk Management:**
   - Risk identification and quantification
   - Impact analysis
   - Mitigation strategy development

4. **Earned Value Management:**
   - CPI, SPI, EAC, ETC calculations
   - Performance forecasting
   - Budget variance analysis

5. **Data Visualization:**
   - Professional charts and graphs
   - Statistical plots
   - Sensitivity analysis (tornado charts)

6. **Technical Skills:**
   - Python programming
   - Data analysis (NumPy, Pandas)
   - Scientific computing
   - Version control (Git)

---

## 📄 License

This project is created for educational purposes as part of the Software Project Management course at [University Name].

**Academic Integrity:** This work represents original analysis and implementation. While the methodology follows industry best practices and academic literature, all code and analysis are original work.

---

## 👥 Contributors

**Student Name:** [Umar Siddique]  
**Roll Number:** [B22F0014SE045]  
**Section:** BS SE (Red + Green) F22  
**Course:** Software Project Management  
**Instructor:** Ms. Isra Zafat  
**Semester:** Fall 2025

---

## 📞 Contact

For questions about this project:
- **Email:** [grbd4114@gmail.com]
- **GitHub:** https://github.com/umar-4114/SPM-Assignment-04

---

## 🙏 Acknowledgments

- **Literature:** Monte Carlo methods from PMI PMBOK Guide
- **Tools:** Open-source Python scientific computing ecosystem
- **Data:** Inspired by real-world Agile project patterns

---

**Last Updated:** December 2025  
**Version:** 1.0  
**Status:** Complete ✅

---

*This simulation provides statistical insights into project outcomes and should be used alongside professional judgment and domain expertise for project planning decisions.*
