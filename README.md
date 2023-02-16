# Landscaping project

Репозиторий проекта НИР: № 622263 «Планирование видового состава городских зеленых насаждений при помощи сетевого моделирования».

## Structure

- **database** - database descrpition, data insertion scripts and other
- **photos** - plants photos hosting docker service and photos preparation/insertion scripts
- **method** - method explanation, graphs, compositions and utility scripts

## Description

In this project we propose the plants composition algorithm which can generate new sets of recommended plant species for green areas or update sets for existing ones. This algorithm accounts for a number of external and internal natural and anthropogenic factors, for example, light conditions, interspecies compatability or soil salinization. Algorithm's pipeline consists of two main steps: spatial analysis block where suitable species are selected, and ecological network analysis block where community partition method is used on species interaction graph to generate several compositions of plants.
We also provide methods of knowledge database creation and spatial environmental data collection.

## General scheme of work

![General scheme of work](https://news.egov.itmo.ru/photo/algoritm_nahozhdeniya_kompozicij_rastenij-1.png) 

## Example

Scripts for step 0 are in the "database" folder, steps 1-8 can be done with update_current_composition, get_recommended_composition or get_composition_unknown functions from method/get_composition.py

0. Create knowledge database
1. Generate compatability graph based on knowledge database
![compatability](landscaping/docs/compatability_graph.png) 

2. Select an area for composition generation
![Example](https://news.egov.itmo.ru/photo/2023-02-15_131219.jpg) 

3. Download light conditions
4. Download external limitation factors
![Example](https://news.egov.itmo.ru/photo/2023-02-15_131219.jpg) 

5. Select a list of species which have suitable light conditions in this area and resistant for limitation factors
6. Generate a subgraph of compatability graph with selected species as nodes
![Example](https://news.egov.itmo.ru/photo/2023-02-15_131219.jpg) 

7. Use community partition method to create compositions
Var 1:
![Example](https://news.egov.itmo.ru/photo/2023-02-15_131219.jpg) 
Var 2:
![Example](https://news.egov.itmo.ru/photo/2023-02-15_131219.jpg) 

8. Done!

 
