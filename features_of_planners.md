The original repo: https://github.com/IBM/forbiditerative



# Top K planner

Return a number of k, best quality (with lowest cost) plans

We used this in the AAMAS paper

# Top quality

Set a quality boundary (e.g. 1.1)

Return all the plans which costs are less than 1.1*the_lowest_cost_plan

Equals to the 10% sub-optimality dataset in the AAMAS paper

# Diverse planner

There are 3 available planners:

1. diverse_agl

   Similar to top-k planner, from the lowest cost plan to higher cost plans

   Set of actions must be different (if a plan reorder its action sequence, that's only counted as 1 plan)

   ```
   # ./plan_diverse_agl.sh <domain> <problem> <number-of-plans>
   ./plan_diverse_agl.sh examples/logistics00/domain.pddl examples/logistics00/probLOGISTICS-4-0.pddl 10
   ```

   

2. diverse_sat

   Post-processed the founded plans from diverse_agl according to a metric (stability, uniqueness, state).

   Using a greedy algorithm, add a plan to the set if that plan can maximize the metric.

   ```
   ## See the dependencies below (1 and 2)
   # ./plan_diverse_sat.sh <domain> <problem> <number-of-plans> <diversity-metric> <larger-number-of-plans>
   ./plan_diverse_sat.sh examples/logistics00/domain.pddl examples/logistics00/probLOGISTICS-4-0.pddl 10 stability 20
   ```

   Using the diverse_agl to generate 20 plans. Then from these 20 plans, select 10 plans can maximizing the metric (greedy)

   

3. diverse_bD

   Post-processed the founded plans from diverse_agl according to a metric (stability, uniqueness, state).

   Set a boundary of metric, if a plan can satisfy the boundary requirement, then it will be add into the output set.

   ```
   ## See the dependencies below (1, 2, and 3)
   # ./plan_diverse_bounded.sh <domain> <problem> <number-of-plans> <diversity-metric> <bound> <larger-number-of-plans>
   ./plan_diverse_bounded.sh examples/logistics00/domain.pddl examples/logistics00/probLOGISTICS-4-0.pddl 10 stability 0.25 20
   ```



Metrics:

stability: 

measures the ratio of the number of actions that appear on both plans to the total number of actions on these plans. 

A($\pi$) is the set of actions in $\pi$.


$$
sim_{stability}=\frac{|A(\pi)\cap A(\pi')|}{|A(\pi)\cup A(\pi')|}
$$
Uniqueness:

It is another measure that considers plans as action sets. It measures whether two plans are permutations of each other, or one plan is a partial plan (subset) of the other plan.

Roberts, M.; Howe, A. E.; and Ray, I. 2014. Evaluating diversity
in classical planning. In Chien, S.; Fern, A.; Ruml,
W.; and Do, M., eds., Proceedings of the Twenty-Fourth International
Conference on Automated Planning and Scheduling
(ICAPS 2014), 253–261. AAAI Press.





