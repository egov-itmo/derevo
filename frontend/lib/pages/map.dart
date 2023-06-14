import 'package:flutter/material.dart';
import 'package:landscaping_frontend/notifiers/compositions.dart';
import 'package:landscaping_frontend/pages/plants_list.dart';
import 'package:landscaping_frontend/widgets/choose_options.dart';
import 'package:landscaping_frontend/widgets/landscape_map.dart';
import 'package:provider/provider.dart';

import '../models/plants.dart';

class MapPage extends StatelessWidget {
  const MapPage({super.key});

  @override
  Widget build(BuildContext context) {
    var compositionsModel = context.watch<CompositionsModel>();
    List<Plants>? compositions = compositionsModel.compositions?.compositions;
    ThemeData theme = Theme.of(context);

    void closeCallback() {
      compositionsModel.compositions = null;
    }

    return Consumer<CompositionsModel>(
      builder: (context, value, child) => Stack(
        children: [
          const LandscapeMap(),
          Positioned(
            right: 40,
            top: 40,
            width: 300,
            child: ChooseOptions(theme: theme),
          ),
          if (compositions != null)
            Center(
              child: ResultsTable(
                  compositions: compositions, close: closeCallback),
            )
        ],
      ),
    );
  }
}

class ResultsTable extends StatelessWidget {
  const ResultsTable(
      {super.key, required this.compositions, required this.close});

  final List<Plants> compositions;
  final void Function() close;

  @override
  Widget build(BuildContext context) {
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
                  alignment: Alignment.centerRight,
                  child: ElevatedButton(
                      onPressed: close,
                      child: Icon(
                        Icons.cancel_presentation_outlined,
                        color: Colors.red.shade400,
                      )),
                ),
              ),
            ),
          ),
          Expanded(
            child: Container(
              color: Colors.green.shade200,
              child: SingleChildScrollView(
                scrollDirection: Axis.vertical,
                child: PlantsTable(
                  compositions[0].plants,
                  withSwitch: false,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
