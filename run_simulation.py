"""
SPM Assignment 04: Agile Software Delivery Simulation
Comprehensive Monte Carlo Simulation Script

This script runs the complete simulation and generates all required outputs.
It can be run standalone or executed cell-by-cell in a Jupyter notebook.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from scipy import stats
from collections import defaultdict
import warnings
import pickle
import os

warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

# Configure plotting
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory
os.makedirs('output', exist_ok=True)

print("="*60)
print("SPM ASSIGNMENT 04: AGILE SOFTWARE DELIVERY SIMULATION")
print("="*60)
print("\n✓ Libraries imported successfully")

# =============================================================================
# SECTION 1: PROJECT PLANNING AND SETUP
# =============================================================================

print("\n" + "="*60)
print("SECTION 1: PROJECT PLANNING AND SETUP")
print("="*60)

# Load data
print("\nLoading project data...")
backlog_df = pd.read_csv('data/backlog.csv')
print(f"  ✓ Backlog: {len(backlog_df)} user stories")

with open('data/teams.json', 'r') as f:
    teams_data = json.load(f)
print(f"  ✓ Teams: {len(teams_data['teams'])} teams")

with open('data/risks.json', 'r') as f:
    risks_data = json.load(f)
print(f"  ✓ Risks: {len(risks_data['risks'])} risks")

# Analyze backlog
total_story_points = backlog_df['Story Points'].sum()
avg_tech_debt = backlog_df['Technical Debt Factor'].mean()

print(f"\nBacklog Analysis:")
print(f"  Total Story Points: {total_story_points}")
print(f"  Average Technical Debt Factor: {avg_tech_debt:.2%}")

# Complexity breakdown
complexity_breakdown = backlog_df.groupby('Complexity')['Story Points'].agg(['count', 'sum'])
print(f"\nComplexity Distribution:")
print(complexity_breakdown)

# Priority breakdown
priority_breakdown = backlog_df.groupby('Priority')['Story Points'].sum()
print(f"\nPriority Distribution:")
print(priority_breakdown)

# Dependencies
def parse_dependencies(dep_str):
    if pd.isna(dep_str) or dep_str == '':
        return []
    return [d.strip() for d in str(dep_str).split('|')]

backlog_df['Parsed_Dependencies'] = backlog_df['Dependencies'].apply(parse_dependencies)
backlog_df['Dependency_Count'] = backlog_df['Parsed_Dependencies'].apply(len)

print(f"\nDependency Analysis:")
print(f"  Stories with dependencies: {len(backlog_df[backlog_df['Dependency_Count'] > 0])}")
print(f"  Stories ready to start: {len(backlog_df[backlog_df['Dependency_Count'] == 0])}")

# Team configuration
teams = teams_data['teams']
total_velocity = sum(team['average_velocity'] for team in teams)
total_cost = sum(team['cost_per_sprint'] for team in teams)

print(f"\nTeam Configuration:")
for team in teams:
    print(f"  {team['team_name']}: {team['average_velocity']} SP/sprint, ${team['cost_per_sprint']:,}/sprint")
print(f"  Combined Velocity: {total_velocity} SP/sprint")
print(f"  Combined Cost: ${total_cost:,}/sprint")

# Baseline estimates
baseline_sprints = np.ceil(total_story_points / total_velocity)
baseline_cost = baseline_sprints * total_cost

print(f"\nBaseline Estimates (ideal scenario):")
print(f"  Estimated Sprints: {baseline_sprints:.0f}")
print(f"  Estimated Cost: ${baseline_cost:,.0f}")
print(f"  Estimated Duration: {baseline_sprints * 2:.0f} weeks")

# Simulation configuration
SIMULATION_CONFIG = {
    'num_simulations': 1000,
    'sprint_duration_weeks': 2,
    'min_sprints': 10,
    'max_sprints': 50,
    'scope_change_sprint': 5,
    'scope_change_points': 58,
    'technical_debt_accumulation_rate': 0.02,
    'resource_contention_probability': 0.25,
    'resource_contention_impact': 0.10,
}

TEAMS_CONFIG = teams
RISKS_CONFIG = risks_data['risks']

print(f"\n✓ Section 1 Complete")

# =============================================================================
# SECTION 2: VELOCITY, RESOURCE, AND TECHNICAL DEBT MODELING
# =============================================================================

print("\n" + "="*60)
print("SECTION 2: VELOCITY AND TECHNICAL DEBT MODELING")
print("="*60)

def simulate_sprint_velocity(team, sprint_num, technical_debt_factor, resource_contention=False):
    """Simulate team velocity for a single sprint"""
    base_velocity = np.random.normal(team['average_velocity'], team['velocity_std'])
    base_velocity = max(0, base_velocity)
    effective_velocity = base_velocity * (1 - technical_debt_factor)
    if resource_contention:
        effective_velocity *= (1 - SIMULATION_CONFIG['resource_contention_impact'])
    return effective_velocity

def calculate_technical_debt(completed_points):
    """Calculate cumulative technical debt factor"""
    avg_debt = avg_tech_debt
    cumulative_debt = avg_debt * (1 + SIMULATION_CONFIG['technical_debt_accumulation_rate'])
    return min(cumulative_debt, 0.30)

def check_resource_contention():
    """Check if resource contention occurs"""
    return np.random.random() < SIMULATION_CONFIG['resource_contention_probability']

print("\n✓ Velocity simulation functions defined")

# Test velocity simulation
test_team = TEAMS_CONFIG[0]
test_velocities = [simulate_sprint_velocity(test_team, 1, 0.0, False) for _ in range(100)]
print(f"\nTest: {test_team['team_name']}")
print(f"  Simulated mean velocity: {np.mean(test_velocities):.2f} SP")
print(f"  Expected: {test_team['average_velocity']} SP")

print(f"\n✓ Section 2 Complete")

# =============================================================================
# SECTION 3: RISK AND SCOPE MANAGEMENT
# =============================================================================

print("\n" + "="*60)
print("SECTION 3: RISK AND SCOPE MANAGEMENT")
print("="*60)

def check_risk_occurrence(risk, sprint_num):
    """Check if a risk occurs based on probability"""
    return np.random.random() < risk['probability']

def apply_risk_impact(risk, current_velocity, current_cost, sprint_num, risk_active_sprints):
    """Apply risk impact based on type"""
    risk_id = risk['risk_id']
    impact_type = risk['impact_type']
    impact_value = risk['impact_value']
    
    modified_velocity = current_velocity
    modified_cost = current_cost
    delay_sprints = 0
    
    if risk_id in risk_active_sprints and risk_active_sprints[risk_id] > 0:
        risk_active_sprints[risk_id] -= 1
        if impact_type == 'velocity_reduction':
            modified_velocity = current_velocity * (1 - impact_value)
    else:
        if impact_type == 'velocity_reduction':
            modified_velocity = current_velocity * (1 - impact_value)
            duration = risk.get('duration_sprints', 1)
            risk_active_sprints[risk_id] = duration - 1
        elif impact_type == 'cost_increase':
            if isinstance(impact_value, float) and impact_value < 1:
                modified_cost = current_cost * (1 + impact_value)
            else:
                modified_cost = current_cost + impact_value
        elif impact_type == 'delay':
            delay_sprints = int(impact_value)
    
    return modified_velocity, modified_cost, delay_sprints, risk_active_sprints

print("\n✓ Risk simulation functions defined")

# Test risk occurrence
print("\nRisk probability test (100 sprints):")
for risk in RISKS_CONFIG[:3]:
    occurrences = sum(check_risk_occurrence(risk, i) for i in range(100))
    print(f"  {risk['risk_name']}: {occurrences}% (expected {risk['probability']*100:.0f}%)")

print(f"\n✓ Section 3 Complete")

# =============================================================================
# SECTION 4: MONTE CARLO SIMULATION
# =============================================================================

print("\n" + "="*60)
print("SECTION 4: MONTE CARLO SIMULATION")
print("="*60)

def run_single_simulation(sim_id, backlog_df, teams, risks, config):
    """Run a single simulation iteration"""
    remaining_points = total_story_points
    completed_points = 0
    current_sprint = 0
    total_cost = 0
    technical_debt = 0
    risk_active_sprints = {}
    delays_accumulated = 0
    sprint_data = []
    risks_occurred = []
    scope_change_applied = False
    
    while remaining_points > 0 and current_sprint < config['max_sprints']:
        current_sprint += 1
        
        if current_sprint == config['scope_change_sprint'] and not scope_change_applied:
            remaining_points += config['scope_change_points']
            scope_change_applied = True
        
        if delays_accumulated > 0:
            delays_accumulated -= 1
            sprint_data.append({
                'sprint': current_sprint, 'velocity': 0, 'completed': 0,
                'remaining': remaining_points, 'cost': 0,
                'technical_debt': technical_debt, 'delayed': True
            })
            continue
        
        technical_debt = calculate_technical_debt(completed_points)
        has_contention = check_resource_contention()
        
        sprint_velocity_total = 0
        sprint_cost_total = 0
        
        for team in teams:
            team_velocity = simulate_sprint_velocity(team, current_sprint, technical_debt, has_contention)
            team_cost = team['cost_per_sprint']
            
            for risk in risks:
                if check_risk_occurrence(risk, current_sprint):
                    team_velocity, team_cost, delay, risk_active_sprints = apply_risk_impact(
                        risk, team_velocity, team_cost, current_sprint, risk_active_sprints
                    )
                    if delay > 0:
                        delays_accumulated += delay
                    risks_occurred.append({
                        'sprint': current_sprint, 'risk': risk['risk_name'],
                        'impact': risk['impact_description']
                    })
            
            sprint_velocity_total += team_velocity
            sprint_cost_total += team_cost
        
        points_completed = min(sprint_velocity_total, remaining_points)
        remaining_points -= points_completed
        completed_points += points_completed
        total_cost += sprint_cost_total
        
        sprint_data.append({
            'sprint': current_sprint, 'velocity': sprint_velocity_total,
            'completed': points_completed, 'remaining': remaining_points,
            'cost': sprint_cost_total, 'technical_debt': technical_debt,
            'delayed': False
        })
    
    return {
        'sim_id': sim_id, 'total_sprints': current_sprint, 'total_cost': total_cost,
        'completed_points': completed_points, 'risks_occurred': len(risks_occurred),
        'sprint_data': sprint_data, 'risks_detail': risks_occurred,
        'scope_change_applied': scope_change_applied
    }

# Run simulations
print(f"\nRunning {SIMULATION_CONFIG['num_simulations']} Monte Carlo simulations...")
print("This will take a few minutes...\n")

simulation_results = []
for sim_id in range(SIMULATION_CONFIG['num_simulations']):
    if (sim_id + 1) % 100 == 0:
        print(f"  Progress: {sim_id + 1}/{SIMULATION_CONFIG['num_simulations']}")
    result = run_single_simulation(sim_id, backlog_df, TEAMS_CONFIG, RISKS_CONFIG, SIMULATION_CONFIG)
    simulation_results.append(result)

sprints_to_completion = [r['total_sprints'] for r in simulation_results]
total_costs = [r['total_cost'] for r in simulation_results]
risks_occurred_counts = [r['risks_occurred'] for r in simulation_results]

print(f"\n✓ All simulations completed!")

print("\nResults Summary:")
print(f"  Sprints - Mean: {np.mean(sprints_to_completion):.2f}, Median: {np.median(sprints_to_completion):.2f}")
print(f"  Cost - Mean: ${np.mean(total_costs):,.0f}, Median: ${np.median(total_costs):,.0f}")
print(f"  Risks - Mean occurrences: {np.mean(risks_occurred_counts):.2f}")

# Confidence intervals
print("\nConfidence Intervals:")
sprints_sorted = np.sort(sprints_to_completion)
ci_50 = (np.percentile(sprints_sorted, 25), np.percentile(sprints_sorted, 75))
ci_80 = (np.percentile(sprints_sorted, 10), np.percentile(sprints_sorted, 90))
ci_95 = (np.percentile(sprints_sorted, 2.5), np.percentile(sprints_sorted, 97.5))

print(f"  50% CI: {ci_50[0]:.1f} - {ci_50[1]:.1f} sprints")
print(f"  80% CI: {ci_80[0]:.1f} - {ci_80[1]:.1f} sprints")
print(f"  95% CI: {ci_95[0]:.1f} - {ci_95[1]:.1f} sprints")

baseline_prob = np.sum(np.array(sprints_to_completion) <= baseline_sprints) / len(sprints_to_completion)
print(f"\nProbability of baseline completion: {baseline_prob:.1%}")

print(f"\n✓ Section 4 Complete")

# =============================================================================
# SECTION 5: SENSITIVITY ANALYSIS
# =============================================================================

print("\n" + "="*60)
print("SECTION 5: SENSITIVITY ANALYSIS")
print("="*60)

print("\nAnalyzing ±20% variation in key parameters...")

sensitivity_params = {
    'team_velocity': {
        'description': 'Team Average Velocity',
        'base_value': np.mean([t['average_velocity'] for t in TEAMS_CONFIG]),
    },
    'velocity_std': {
        'description': 'Velocity Standard Deviation',
        'base_value': np.mean([t['velocity_std'] for t in TEAMS_CONFIG]),
    },
}

sensitivity_results = {}
num_sens_sims = 100

for param_name, param_info in sensitivity_params.items():
    print(f"\nTesting {param_info['description']}...")
    
    # Low variation
    if param_name == 'team_velocity':
        teams_low = [dict(t, average_velocity=t['average_velocity'] * 0.8) for t in TEAMS_CONFIG]
        teams_high = [dict(t, average_velocity=t['average_velocity'] * 1.2) for t in TEAMS_CONFIG]
    else:
        teams_low = [dict(t, velocity_std=t['velocity_std'] * 0.8) for t in TEAMS_CONFIG]
        teams_high = [dict(t, velocity_std=t['velocity_std'] * 1.2) for t in TEAMS_CONFIG]
    
    low_results = [run_single_simulation(0, backlog_df, teams_low, RISKS_CONFIG, SIMULATION_CONFIG)['total_sprints']
                   for _ in range(num_sens_sims)]
    high_results = [run_single_simulation(0, backlog_df, teams_high, RISKS_CONFIG, SIMULATION_CONFIG)['total_sprints']
                    for _ in range(num_sens_sims)]
    
    low_mean = np.mean(low_results)
    high_mean = np.mean(high_results)
    impact = abs(high_mean - low_mean)
    
    sensitivity_results[param_name] = {
        'description': param_info['description'],
        'base_value': param_info['base_value'],
        'low_sprints': low_mean,
        'high_sprints': high_mean,
        'impact': impact
    }
    
    print(f"  Low (-20%): {low_mean:.2f} sprints")
    print(f"  High (+20%): {high_mean:.2f} sprints")
    print(f"  Impact: {impact:.2f} sprints")

print(f"\n✓ Section 5 Complete")

# =============================================================================
# GENERATE VISUALIZATIONS
# =============================================================================

print("\n" + "="*60)
print("GENERATING VISUALIZATIONS")
print("="*60)

# 1. Backlog Analysis
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

axes[0, 0].hist(backlog_df['Story Points'], bins=7, edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Story Points')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].set_title('Story Points Distribution')
axes[0, 0].grid(True, alpha=0.3)

complexity_counts = backlog_df['Complexity'].value_counts()
axes[0, 1].bar(complexity_counts.index, complexity_counts.values, edgecolor='black', alpha=0.7)
axes[0, 1].set_title('Complexity Distribution')
axes[0, 1].grid(True, alpha=0.3, axis='y')

priority_counts = backlog_df['Priority'].value_counts()
axes[1, 0].pie(priority_counts.values, labels=priority_counts.index, autopct='%1.1f%%')
axes[1, 0].set_title('Priority Distribution')

axes[1, 1].hist(backlog_df['Technical Debt Factor'], bins=20, edgecolor='black', alpha=0.7)
axes[1, 1].axvline(avg_tech_debt, color='red', linestyle='--', linewidth=2, label=f'Mean: {avg_tech_debt:.2%}')
axes[1, 1].set_xlabel('Technical Debt Factor')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Technical Debt Distribution')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/backlog_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ backlog_analysis.png")

# 2. Monte Carlo Completion
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].hist(sprints_to_completion, bins=30, edgecolor='black', alpha=0.7, color='skyblue')
axes[0].axvline(np.mean(sprints_to_completion), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(sprints_to_completion):.1f}')
axes[0].axvline(baseline_sprints, color='orange', linestyle='--', linewidth=2, label=f'Baseline: {baseline_sprints:.0f}')
axes[0].set_xlabel('Sprints to Completion')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Project Completion Distribution')
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='y')

axes[1].hist(total_costs, bins=30, edgecolor='black', alpha=0.7, color='lightcoral')
axes[1].axvline(np.mean(total_costs), color='red', linestyle='--', linewidth=2, label=f'Mean: ${np.mean(total_costs):,.0f}')
axes[1].set_xlabel('Total Project Cost ($)')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Project Cost Distribution')
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('output/monte_carlo_completion.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ monte_carlo_completion.png")

# 3. Monte Carlo Cost
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(total_costs, bins=30, edgecolor='black', alpha=0.7, color='lightcoral')
ax.axvline(np.mean(total_costs), color='red', linestyle='--', linewidth=2, label=f'Mean: ${np.mean(total_costs):,.0f}')
ax.set_xlabel('Total Project Cost ($)')
ax.set_ylabel('Frequency')
ax.set_title('Cost Distribution')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('output/monte_carlo_cost.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ monte_carlo_cost.png")

# 4. Burndown Chart
median_idx = np.argsort(sprints_to_completion)[len(sprints_to_completion)//2]
rep_sim = simulation_results[median_idx]

sprint_nums = [0] + [d['sprint'] for d in rep_sim['sprint_data']]
total_with_scope = total_story_points + SIMULATION_CONFIG['scope_change_points']
remaining_work = [total_with_scope] + [d['remaining'] for d in rep_sim['sprint_data']]

ideal_line = [total_with_scope - (total_with_scope / (len(sprint_nums)-1)) * i for i in range(len(sprint_nums))]

fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(sprint_nums, remaining_work, marker='o', linewidth=2, markersize=4, label='Actual', color='blue')
ax.plot(sprint_nums, ideal_line, linestyle='--', linewidth=2, label='Ideal', color='green', alpha=0.7)
ax.axvline(SIMULATION_CONFIG['scope_change_sprint'], color='red', linestyle='--', alpha=0.5, label='Scope Change')
ax.set_xlabel('Sprint Number')
ax.set_ylabel('Remaining Story Points')
ax.set_title('Burndown Chart - Representative Simulation')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output/burndown_chart.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ burndown_chart.png")

# 5. Velocity Trend
velocity_per_sprint = [d['velocity'] for d in rep_sim['sprint_data']]

fig, ax = plt.subplots(figsize=(12, 7))
ax.bar(sprint_nums[1:], velocity_per_sprint, alpha=0.6, label='Sprint Velocity', color='skyblue', edgecolor='black')
ax.axhline(total_velocity, color='green', linestyle='--', linewidth=2, label=f'Expected: {total_velocity} SP', alpha=0.7)
ax.set_xlabel('Sprint Number')
ax.set_ylabel('Velocity (Story Points)')
ax.set_title('Team Velocity Over Time')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('output/velocity_trend.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ velocity_trend.png")

# 6. Earned Value
cumulative_completed = []
cumulative_cost = []
total_completed = 0
total_spent = 0

for d in rep_sim['sprint_data']:
    total_completed += d['completed']
    total_spent += d['cost']
    cumulative_completed.append(total_completed)
    cumulative_cost.append(total_spent)

sprints = sprint_nums[1:]
pv_per_sprint = total_with_scope / len(sprints)
planned_value = [pv_per_sprint * (i + 1) for i in range(len(sprints))]
earned_value = cumulative_completed.copy()

current_ev = earned_value[-1]
current_ac = cumulative_cost[-1]
current_pv = planned_value[-1]
cpi = current_ev / current_ac * (total_cost / total_with_scope)
spi = current_ev / current_pv if current_pv > 0 else 1.0

fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(sprints, planned_value, marker='s', linewidth=2, markersize=5, label='PV', color='blue')
ax.plot(sprints, earned_value, marker='o', linewidth=2, markersize=5, label='EV', color='green')
ax2 = ax.twinx()
ax2.plot(sprints, [c/1000 for c in cumulative_cost], marker='^', linewidth=2, markersize=5, label='AC', color='red')
ax.set_xlabel('Sprint')
ax.set_ylabel('Story Points')
ax2.set_ylabel('Cost ($1000s)')
ax.set_title(f'Earned Value Management (CPI: {cpi:.2f}, SPI: {spi:.2f})')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output/earned_value.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ earned_value.png")

# 7. Risk Impact
all_risks_data = []
for result in simulation_results:
    all_risks_data.extend(result['risks_detail'])

if all_risks_data:
    risks_df = pd.DataFrame(all_risks_data)
    risk_counts = risks_df['risk'].value_counts()
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    axes[0].barh(risk_counts.index, risk_counts.values, color='coral', edgecolor='black')
    axes[0].set_xlabel('Occurrences')
    axes[0].set_ylabel('Risk')
    axes[0].set_title('Risk Occurrence Frequency')
    axes[0].grid(True, alpha=0.3, axis='x')
    
    risk_names = [r['risk_name'] for r in RISKS_CONFIG]
    risk_probs = [r['probability'] * 100 for r in RISKS_CONFIG]
    
    axes[1].bar(range(len(risk_names)), risk_probs, color='steelblue', edgecolor='black', alpha=0.7)
    axes[1].set_xticks(range(len(risk_names)))
    axes[1].set_xticklabels(risk_names, rotation=45, ha='right')
    axes[1].set_ylabel('Probability (%)')
    axes[1].set_title('Risk Probability Profile')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('output/risk_impact.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ risk_impact.png")

# 8. Sensitivity Tornado
sorted_params = sorted(sensitivity_results.items(), key=lambda x: x[1]['impact'], reverse=True)
param_names = [item[1]['description'] for item in sorted_params]
impacts_low = [baseline_sprints - item[1]['low_sprints'] for item in sorted_params]
impacts_high = [item[1]['high_sprints'] - baseline_sprints for item in sorted_params]

fig, ax = plt.subplots(figsize=(12, 8))
y_pos = np.arange(len(param_names))
ax.barh(y_pos, impacts_low, align='center', color='lightcoral', edgecolor='black', label='-20%', alpha=0.8)
ax.barh(y_pos, impacts_high, align='center', color='lightblue', edgecolor='black', label='+20%', alpha=0.8, left=0)
ax.axvline(0, color='black', linewidth=2, linestyle='--', label='Baseline')
ax.set_yticks(y_pos)
ax.set_yticklabels(param_names)
ax.set_xlabel('Impact on Duration (Sprints)')
ax.set_title('Sensitivity Analysis - Tornado Chart')
ax.legend()
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('output/sensitivity_tornado.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ sensitivity_tornado.png")

# 9. Velocity Distributions
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for idx, team in enumerate(TEAMS_CONFIG):
    velocities = [simulate_sprint_velocity(team, 1, 0.0, False) for _ in range(1000)]
    axes[idx].hist(velocities, bins=30, edgecolor='black', alpha=0.7, density=True)
    axes[idx].axvline(team['average_velocity'], color='red', linestyle='--', linewidth=2, label=f"Expected: {team['average_velocity']}")
    axes[idx].set_xlabel('Story Points')
    axes[idx].set_ylabel('Density')
    axes[idx].set_title(f"{team['team_name']} Velocity")
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output/velocity_distributions.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ velocity_distributions.png")

print("\n✓ All visualizations generated")

# Save simulation data
with open('output/simulation_results.pkl', 'wb') as f:
    pickle.dump({
        'simulation_results': simulation_results,
        'sensitivity_results': sensitivity_results,
        'config': SIMULATION_CONFIG
    }, f)

summary_df = pd.DataFrame({
    'Metric': ['Mean Sprints', 'Median Sprints', 'Mean Cost', 'Median Cost', 'Baseline Sprints', 'Baseline Cost'],
    'Value': [np.mean(sprints_to_completion), np.median(sprints_to_completion), 
              np.mean(total_costs), np.median(total_costs), baseline_sprints, baseline_cost]
})
summary_df.to_csv('output/simulation_summary.csv', index=False)

print("\n" + "="*60)
print("SIMULATION COMPLETE!")
print("="*60)
print("\nAll outputs saved to output/ directory")
print(f"  - 9 visualization files (PNG)")
print(f"  - simulation_results.pkl (raw data)")
print(f"  - simulation_summary.csv (statistics)")
