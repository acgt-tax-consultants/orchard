# orchard
A pipeline creation framework for simplifying reruns and branching

[![Build Status](https://travis-ci.org/acgt-tax-consultants/orchard.svg?branch=master)](https://travis-ci.org/acgt-tax-consultants/orchard)


# Basic Luigi Commands

```
luigid - runs the gui through local host
    just type on browser (to access): localhost:8082

Running:
    python fileWithModule.py moduleName --parameterName1 parameterName1Value
                                        --parameterName2 parameterName2Value...
```


Installation (Development mode [after setting up your environment](https://github.com/acgt-tax-consultants/gitting-started)):
```bash
$ git clone https://github.com/(your_username)/orchard.git
$ cd orchard
$ pip install -e .
```

---

How to run sample pipeline

In one tab (as `luigid` blocks, and `luigid --background` is a pain to kill)
```bash
$ luigid
```

In a separate tab
```bash
$ cd example
$ orchard build test.yml -o out.py
$ orchard launch out.py ModuleThree
```
