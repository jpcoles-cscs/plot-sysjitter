# plot-sysjitter

Graph the results measuring system jitter due to interrupts.

# Dependencies

The plotting routine reads the output of the sysjitter program.

[https://github.com/alexeiz/sysjitter](https://github.com/alexeiz/sysjitter)

# Usage

First run `sysjitter` and the `find-freezable` script
```shell
./find-freezable > freezable.out
./sysjitter --runtime 60 --verbose 300 > summary.txt
```

Next, provide the two output files as input to `plot-sysjitter` and provide an output file for the graph.

```shell
plot-sysjitter <sysjitter-summary.txt> <freezable.out> <output.pdf>
```
