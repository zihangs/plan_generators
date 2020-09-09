# Configurable Parameters (Planners + Miners)

Param:

|                      | Directly Flow Miner                                          | Transition System Miner                                      | Split Miner                                                  | Inductive Miner                                              |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Top-k                | **k**: number of plans<br />**t**: threshold                 | **k**: number of plans<br />                                 | **k**: number of plans                                       | **k**: number of plans<br />**t**: threshold                 |
| Top-q<br />ordered   | **q**: quality<br />**t**: threshold                         | **q**: quality<br />                                         | **q**: quality                                               | **q**: quality<br />**t**: threshold                         |
| Top-q<br />unordered | **q**: quality<br />**t**: threshold                         | **q**: quality<br />                                         | **q**: quality                                               | **q**: quality<br />**t**: threshold                         |
| Diverse agl          | **k**: number of plans<br />**t**: threshold                 | **k**: number of plans<br />                                 | **k**: number of plans                                       | **k**: number of plans<br />**t**: threshold                 |
| Diverse sat          | **k**: number of plans <br />**h**: a larger number<br />**m**: metric name<br />**t**: threshold | **k**: number of plans<br />**h**: a larger number<br />**m**: metric name<br /> | **k**: number of plans<br />**h**: a larger number<br />**m**: metric name | **k**: number of plans<br />**h**: a larger number<br />**m**: metric name<br />**t**: threshold |
| Diverse bD           | **k**: number of plans <br />**h**: a larger number<br />**m**: metric name<br />**b**: bound<br />**t**: threshold | **k**: number of plans<br />**h**: a larger number<br />**m**: metric name<br />**b**: bound<br /> | **k**: number of plans<br />**h**: a larger number<br />**m**: metric name<br />**b**: bound | **k**: number of plans<br />**h**: a larger number<br />**m**: metric name<br />**b**: bound<br />**t**: threshold |

**Notice: the column of Transition System Miner hasn't completed yet. Now, it only contains the parameters from planner side, more parameters from miner side coming soon.**

