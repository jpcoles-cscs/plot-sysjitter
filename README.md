# plot-sysjitter

Graph the results measuring system jitter due to interrupts.

# Dependencies

The plotting routine reads the output of the sysjitter program.

[https://github.com/alexeiz/sysjitter](https://github.com/alexeiz/sysjitter)

# Command Line Arguments (CLAs)
```
Plot system jitter using the output summary of the sysjitter utility

options:
  -h, --help            show this help message and exit
  --summary_file SUMMARY_FILE
                        Path to sysjitter summary file
  --freezable_file FREEZABLE_FILE
                        Path to freezable.out file
  --image_file IMAGE_FILE
                        Path to output image
  --author_name AUTHOR_NAME
                        Name of the author
  --author_email AUTHOR_EMAIL
                        Email of the author
  --plot_title PLOT_TITLE
                        Title of the plot
  --plot_summary PLOT_SUMMARY
                        Summary string of the plot
```

# Usage

First run `sysjitter` 
```shell
./sysjitter --runtime 60 --verbose 300 > summary.txt
```

Next, provide the two output files as input to `plot-sysjitter` and provide an output file for the graph.

```shell
./plot-sysjitter --summary_file ./summary.txt --image_file ./jitter_study.png --author_name Ed --author_email ed@edmole.com 
```
