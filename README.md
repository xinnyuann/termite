# Termite

## Why this fork? Why Termite?

This is a fork project of Termite from https://github.com/sailuh/termite , which is originally developed by Chuang et al [1] without maintainance since 2019. Termite is a visualization tool for inspecting the output of statistical topic models such as Latent Dirichlet allocation (LDA) using an interactive interface as shown above. Termite is an alternative to lists of per-topic words, the standard practice: Users can drill down to examine a specific topic by clicking on a circle or topic label in the matrix, revealing the word-frequency view. The order of the terms presented in this view also uses `seriation`, which accounts for co-occurrence and collocation likelihood between all pairs of words. Term probabilities are encoded in circles. For more details, see Chuang et al [1].

![termite_interface_not_loaded](doc/termite_interface.png)

The package was initially developed in Python 2 and further separated out as a stand-alone topic modeling visualization tool by [Software Analytics Insight Lab](https://github.com/sailuh/termite). 

At the beginning, I created this fork because of my internship project on topic modeling, when I had hard time finding stunning and self-explanatory visualizations for topic modeling. Over time, I realized how rare and inspiring Termite project is tho still abandoned. My hope is to make it work with Python 3 and meanwhile enhance my "unfinished" internship project ;)


## What's new in this fork?


==============================================================

_(The following README inherit [Software Analytics Insight Lab](https://github.com/sailuh/termite) with minor changes...)_

### Background

The original Termite has two versions: The [first](https://github.com/StanfordHCI/termite) is a single component, and the second contains two components, [a data server](https://github.com/uwdata/termite-data-server) and [visualizations](https://github.com/uwdata/termite-visualizations). Because the later versions add more dependencies to the visualization I chose to fork the first version.


### Setup

To install Termite, you will need JDK (now tested on JDK 19 Updated):

1. Download termite from this git repo. 
2. On a terminal, enter the `termite` folder and type:

```
./setup_offline.sh
```

### Test Run

To launch Termite visualization of a topic-term matrix file:

1. **Provide the necessary input files**. Every termite viz is inside a separate project folder. In this test run we will use `termite/example-project`. For other runs, you can simply create any other folder inside `termite`, and provide as a parameter instead of example-project. You must use the same organization of folders and naming convention as example-project shown here:

```
├── model
│   ├── term-index.txt
│   ├── term-topic-matrix.txt
│   └── topic-index.txt
├── tokens
│   └── tokens.txt

```

* **term-topic-matrix.txt**: a term-topic matrix. The rows are the terms, and the topics the columns. 
* **term-index.txt**: The row names.
* **topic-index.txt**: The column names.

* **tokens.txt**: A tokenized corpus, where every line is a document following this format: row_number`\t`list_of_tokens, where `\t` is the tab symbol. 

2. Run the following to use example-project: 

```
python execute.py example.cfg --data-path example-project
```

 * `--data-path` Is the path, inside the termite folder, your project folder is. 

 3. Termite will then process the input files, and create additional folders inside `example-project`. The final `example-project` folder will have the following organization:

```
├── model
│   ├── term-index.txt
│   ├── term-topic-matrix.txt
│   └── topic-index.txt
├── saliency
│   ├── term-info.json
│   ├── term-info.txt
│   ├── topic-info.json
│   └── topic-info.txt
├── similarity
│   └── combined-g2.txt
├── tokens
│   └── tokens.txt
└── topic-model
    ├── output-topic-keys.txt
    ├── output.model
    ├── text.vectors
    ├── topic-word-weights.txt
    └── word-topic-counts.txt
```

On your terminal within termite repository, run the following: 

```
./example-project/public_html/web.sh
```

4. A local webserver will launch on localhost:8888. Open a web browser and type ` http://localhost:8888/` to see the Termite visualization. You can also copy the `public_html` folder to a remote server to make it accessible on the web.

### F.A.Q.

 * 1. Why must I provide a `tokens.txt`?
   * To display the list of terms when a user clicks a circle, Termite uses `seriation` to order the terms. This method relies on term co-ocurrence in the original document, which is not available in a topic-term matrix. 

### Future Work

This fork is at best a quick hack to bypass the mallet/stmt dependencies thanks to all the hard work of [Software Analytics Insight Lab](https://github.com/sailuh/termite). The wiki project contains an exhaustive explanation of some of the code functionality to make this hack possible. In the future, I intend to remove some of the dead code and functionality to make it work for Python3.  

## References

  [1] [Termite: Visualization Techniques for Assessing Textual Topic Models. Jason Chuang, Christopher D. Manning, Jeffrey Heer. Computer Science Dept, Stanford University.](http://vis.stanford.edu/papers/termite)
