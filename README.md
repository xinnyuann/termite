# Termite

![termite_interface_not_loaded](doc/termite_interface.png)

This is a fork project of Termite by Chuang et al [1].

Termite is a visualization tool for inspecting the output of statistical topic models such as Latent Dirichlet allocation (LDA) using an interactive interface as shown above. Termite is an alternative to lists of per-topic words, the standard practice: Users can drill down to examine a specific topic by clicking on a circle or topic label in the matrix, revealing the word-frequency view. The order of the terms presented in this view also uses `seriation`, which accounts for co-occurrence and collocation likelihood between
all pairs of words. Term probabilities are encoded in circles. For more details, see Chuang et al [1].

This Termite fork differs from the source Termite: Instead of taking as input a single .csv corpus, it also expects a topic-term matrix. As such, a topic modeling algorithm is no longer part of Termite pipeline and must be run separately, affording greater flexibility on the choice of the topic modeling algorithm. The second view mentioned in the paper, showing the representative documents belonging to the topic when clicking on a circle or topic label in the matrix, was not found on the source Termite code, and hence is unavailable in this fork.

## Background

The original Termite has two versions: The [first](https://github.com/StanfordHCI/termite) is a single component, and the second contains two components, [a data server](https://github.com/uwdata/termite-data-server) and [visualizations](https://github.com/uwdata/termite-visualizations). Because the later versions add more dependencies to the visualization I chose to fork the first version.

## Why this fork?

I created this fork because topic modeling visualizations are rare and few and the Termite project was abandoned. Unfortunately, both original versions of Termite binds a user to use [MALLET](http://mallet.cs.umass.edu/) or [STMT (Stanford Topic Modeling Toolkit)](https://nlp.stanford.edu/software/tmt/tmt-0.4/) to obtain the Termite topic visualization. This fork removes this dependency by taking as an additional input a topic-term matrix from the user. 

## Setup

To install Termite, you will need [JDK](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) (last tested on JDK 8 Updated 231):

1. Download [termite](https://github.com/sailuh/termite) from this git repo. 
2. Download [termite_dependencies](https://github.com/sailuh/termite_dependencies), and move the `libraries` folder (not the zip) inside the termite folder of step 1.
3. On a terminal, enter the `termite` folder and type:

```
./setup_offline.sh
```

## Test Run

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

On your terminal, run the following: 

```
./termite/example-project/public_html/web.sh
```

4. A local webserver will launch on localhost:8888. Open a web browser and type ` http://localhost:8888/` to see the Termite visualization. You can also copy the `public_html` folder to a remote server to make it accessible on the web.

## F.A.Q.

 * 1. Why must I provide a `tokens.txt`?
   * To display the list of terms when a user clicks a circle, Termite uses `seriation` to order the terms. This method relies on term co-ocurrence in the original document, which is not available in a topic-term matrix. 

## Future Work

This fork is at best a quick hack to bypass the mallet/stmt dependencies. The wiki project contains an exhaustive explanation of some of the code functionality to make this hack possible. In the future, I intend to remove some of the dead code and functionality that is bypassed of Termite.  

## References

  [1] [Termite: Visualization Techniques for Assessing Textual Topic Models. Jason Chuang, Christopher D. Manning, Jeffrey Heer. Computer Science Dept, Stanford University.](http://vis.stanford.edu/papers/termite)
