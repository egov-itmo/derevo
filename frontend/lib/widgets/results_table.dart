import 'dart:math';

import 'package:flutter/material.dart';
import 'package:landscaping_frontend/models/plants.dart';
import 'package:landscaping_frontend/pages/plants_list.dart';

final _numbersIcons = {
  0: Icons.filter_1,
  1: Icons.filter_2,
  2: Icons.filter_3,
  3: Icons.filter_4,
  4: Icons.filter_5,
  5: Icons.filter_6,
  6: Icons.filter_7,
  7: Icons.filter_8,
  8: Icons.filter_9,
};

class ResultsTable extends StatefulWidget {
  const ResultsTable(
      {super.key, required this.compositions, required this.close});

  final List<Plants> compositions;
  final void Function() close;

  @override
  State<ResultsTable> createState() => _ResultsTableState();
}

class _ResultsTableState extends State<ResultsTable> {
  int currentCompositionIndex = 0;

  @override
  Widget build(BuildContext context) {
    var compositionsButtons = [
      for (int i = 0; i < min(widget.compositions.length, 9); i++)
        ElevatedButton.icon(
            onPressed: () => setState(() {
                  currentCompositionIndex = i;
                }),
            label: Text("${widget.compositions[i].plants.length}"),
            icon: Icon(
              _numbersIcons[i],
              color: i == currentCompositionIndex ? Colors.green : Colors.grey,
            ))
    ];
    return Container(
      color: Colors.grey.shade400.withAlpha(210),
      child: Column(
        children: [
          Container(
            color: const Color.fromARGB(255, 230, 199, 107),
            child: Center(
              child: SizedBox(
                child: Container(
                  height: 40,
                  width: 1172,
                  padding: const EdgeInsets.all(2.0),
                  alignment: Alignment.centerLeft,
                  child: Row(
                    children: [
                      const Text("Композиции: "),
                      for (var button in compositionsButtons) button,
                      const Expanded(child: SizedBox.shrink()),
                      ElevatedButton(
                          onPressed: widget.close,
                          child: Icon(
                            Icons.cancel_presentation_outlined,
                            color: Colors.red.shade400,
                          )),
                    ],
                  ),
                ),
              ),
            ),
          ),
          Expanded(
            child: Container(
              color: Colors.green.shade200,
              child: SingleChildScrollView(
                scrollDirection: Axis.vertical,
                child: Column(
                  children: [
                    const SizedBox(
                      width: 1180,
                      child: Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Text(
                          "Предлагаемый список видов растений является рекомендуемым для"
                          " посадки на конкретной территории, являясь устойчивым к"
                          " действующим условиям и ограничивающим факторам."
                          " Стилистическое применения пользователь выбирает"
                          " самостоятельно.",
                          style: TextStyle(fontSize: 18),
                        ),
                      ),
                    ),
                    PlantsTable(
                      widget.compositions[currentCompositionIndex].plants,
                      withSwitch: false,
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
