# Landscaping project

|           |                                                                                                                                                   |
|----------:|:-------------------------------------------------------------------------------------------------------------------------------------------------:|
| License   | ![Licence](https://img.shields.io/badge/License-MIT-yellow.svg)                                                                                   |
| Languages | [![english](https://img.shields.io/badge/lang-en-red.svg)](README.md) [![russian](https://img.shields.io/badge/lang-ru-yellow.svg)](README_ru.md) |

Repository of science research at ITMO University #622263 "Planning city greenery species composition with using network modeling methods".

## Porject structure

- [**backend**](backend/README.md) - backend service, which provides the access to database plants data (including insertion and updating)
    and keeps database schema syncronized.
- [**frontend**](frontend/README.md) - frontend written on Flutter, which can be compiled to web-interface used with Nginx.
- [**photos**](photos/README.md) - plants photos hosting Docker service and photos preparation/insertion scripts.
- [**method**](method/README.md) - derevo module containing plants compositions generation and graph algorithms.

## Description

In this project we propose the plants composition algorithm which can generate new sets of recommended plant
    species for green areas or update sets for existing ones. This algorithm accounts for a number of external
    and internal natural and anthropogenic factors, for example, light conditions, interspecies compatability
    or soil salinization. Algorithm's pipeline consists of two main steps: spatial analysis block where suitable
    species are selected, and ecological network analysis block where community partition method is used
    on species interaction graph to generate several compositions of plants.

We also provide methods of knowledge database creation and spatial environmental data collection.

The deployed demo frontend instance can be found at https://derevo.idu.actcognitive.org with REST
    API at [/api](https://derevo.idu.actcognitive.org/api/docs) postfix.

The backend is also integrated in Platform of Digital Urbanistic by Laboratory of City Data Analysis of ITMO University. Its frontend page located at
    the https://dc.idu.actcognitive.org/applied-services/greenery.

Service description page available at https://news.egov.itmo.ru/map/dev/index.html.


Method documentation is located at https://derevo.readthedocs.io/en/dev/

## General scheme of work (russian)

![General scheme of work](https://news.egov.itmo.ru/photo/algoritm_nahozhdeniya_kompozicij_rastenij-1.png)

## Publications

The main results of the work are described in following publications list:

1. Value-Oriented Management of City Development Programs Based on Data from Social Networks. Nizomutdinov, B.A., Uglova, A.B., Antonov, A.S. Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics) this link is disabled, 2023, 13957 LNCS, PP 369–382 (Scopus - published)
2. Sergey Mityagin, Nikita Kopyt, Irina А. Shmeleva, Sofia Malysheva, Ekaterina Malysheva, Aleksandr Antonov, Aleksey Sokol, Nikita Zakharenko, Tatiana Churiakova, Semen A. Budennyy, Alexander V. Boukhanovsky. Green Spaces in Urban Environments: Network Planning of Plant Species Composition // Sustainability. 2023 (Scopus - accepted in May 2023)
3. Boris Nizomutdinov and Nikita Kopyt  Planning of the species composition of urban green spaces using network modeling and comments from users of social networks. Internet and Modern Society (IMS-2023) - (text accepted in April 2023, speach in June 2023), included in Injoit cllection - HAC)
4. Boris Nizomutdinov, Nikita Kopyt Development of a network model for urban greening based on the characteristics of plant growth. Young DTGS – 2023 (RSCI)
5. Низомутдинов, Б. А. Планирование видового состава зеленых насаждений на основе текстовых комментариев горожан / Б. А. Низомутдинов, Н. М. Копыть // Управление информационными ресурсами: Материалы XIX Международной научно-практической конференции, Минск, 22 марта 2023 года. – Минск: Академия управления при Президенте Республики Беларусь, 2023. – С. 366-368. (RSCI)

## Example

Scripts for step 0 are in the "database" folder, steps 1-8 can be done with `update_current_composition`,
    `get_recommended_composition` or `get_composition_unknown` functions from [get_composition module](method/get_composition.py).

0. Create knowledge database

1. Generate compatability graph based on knowledge database

    <img src="images/compatability_graph.png" alt="compatability graph" width="50%" height="50%"/>

2. Select an area for composition generation

    <img src="images/green_area.png" alt="area" width="50%" height="50%"/>

3. Download light conditions

4. Download external limitation factor

    <img src="images/limitation_factors.png" alt="limitation factors" width="50%" height="50%"/>

5. Select a list of species which have suitable light conditions in this area and resistant for limitation factors

6. Generate a subgraph of compatability graph with selected species as nodes
    <img src="images/original_graph.png" alt="original subgraph" width="50%" height="50%"/>


7. Use community partition method to create compositions

    - Variant 1:

    <img src="images/updated_graph_1.png" alt="Variant 1" width="50%" height="50%"/>

    - Variant 2:

    <img src="images/updated_graph_2.png" alt="Variant 2" width="50%" height="50%"/>
