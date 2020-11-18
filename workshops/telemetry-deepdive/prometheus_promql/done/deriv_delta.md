# deriv(), delta()
## Goals
The goals of this lab are:
* Familerize yourself with the deriv() function.
* Familerize yourself with the delta() function.

## Excercises
### Per-Second Derivative
Calculate how `disk_used` is evolving per second for all disk paths on `host` `deftlnetops200` averaged over the last 10 minutes.
<details>
  <summary>Reveal Answer</summary>

```
deriv(disk_used{host="deftlnetops200"}[10m])
```
</details>

### Delta 
Calculate the difference in `disk_used` for all disk paths on `host` `deftlnetops200` over a 15 minute period.
<details>
  <summary>Reveal Answer</summary>

```
delta(disk_used{host="deftlnetops200"}[15m])
```
</details>