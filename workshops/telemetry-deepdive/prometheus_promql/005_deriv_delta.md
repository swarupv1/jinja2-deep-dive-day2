# deriv(), delta()
## Goals
The goals of this lab are:
* Familiarize yourself with the deriv() function.
* Familiarize yourself with the delta() function.

## Exercises
### Task 1
Calculate how `disk_used` is evolving per second for all disk paths on `host` `deftlnetops200` averaged over the last 10 minutes.
<details>
  <summary>Reveal Answer</summary>

```
deriv(disk_used{host="deftlnetops200"}[10m])
```
</details>

### Task 2 
Calculate the difference in `disk_used` for all disk paths on `host` `deftlnetops200` over a 15 minute period.
<details>
  <summary>Reveal Answer</summary>

```
delta(disk_used{host="deftlnetops200"}[15m])
```
</details>