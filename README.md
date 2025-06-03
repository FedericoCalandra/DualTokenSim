# DualTokenSim
DualTokenSim is a Python-based simulator designed to study the behavior of dual-token algorithmic stablecoins, with a special focus on modeling normal and stress market conditions. These types of stablecoins aim to maintain a peg without centralized collateral—yet they can be highly susceptible to depegging, as illustrated by the 2022 Terra-Luna collapse (over $50B in market cap lost in days).

This simulator offers a controlled environment to analyze such failures and explore improvements in design and resilience mechanisms.


# ✨ Key Features
🔁 Simulation of automated market makers and user trading behavior

📉 Price dynamics based on stochastic processes

💥 Panic scenarios and cascading effects modeled explicitly

🔍 Realistic replication of the Terra-Luna depeg event

📊 Tools for quantitative stability analysis (e.g. MSE vs. peg)


# 🔬 Research Context
DualTokenSim is part of ongoing research to better understand and design resilient algorithmic stablecoins. It supports the analysis of new dual-token protocol proposals by providing a testbed for:

- Scenario-based design evaluation

- Early detection of instability risks

- Fine-tuning stabilization mechanisms before mainnet deployment

One of the most promising applications of DualTokenSim is its ability to test new dual-token AS protocols under a wide range of market scenarios. By simulating stress conditions and analyzing the performance of proposed designs, developers can identify weaknesses and refine stabilization mechanisms before deploying them in live markets.


# 🧪 Use Case: Terra-Luna Collapse
DualTokenSim successfully replicates the Terra-Luna collapse dynamics, including:

- Depegging triggers

- Exponential LUNA minting

- Users' behavior during panic

- System death spiral

# 📚 Acknowledgments
This work is supported by:

The PRIN 2020 project NiRvAna — "Noninterference and Reversibility Analysis in Private Blockchains"

The Italian PhD Program in Blockchain and Distributed Ledger Technology

Funding from the PNRR — "Piano Nazionale di Ripresa e Resilienza", as per D.M. 118/2023



# Future Work

Key areas for enhancement include:

- Model refinement, based on incorporating more market factors and different arbitrage dynamics for greater realism.
- Validation and improvement proposals, which serve as a testbed for evaluating modifications to the VLP mechanism and new stabilization techniques.
- Automating parameter fine-tuning, by using machine learning or optimization algorithms for more accurate and efficient parameter calibration.
- Quantitative stability evaluation using the Mean Squared Error (MSE) between the stablecoin price and its peg in balanced market scenarios.
- Stress-testing under extreme market conditions, including network congestion, flash crashes, and liquidity shocks.

