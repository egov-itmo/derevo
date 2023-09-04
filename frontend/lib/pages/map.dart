import 'package:flutter/material.dart';
import 'package:landscaping_frontend/models/plants.dart';
import 'package:landscaping_frontend/notifiers/compositions.dart';
import 'package:landscaping_frontend/widgets/choose_options.dart';
import 'package:landscaping_frontend/widgets/landscape_map.dart';
import 'package:landscaping_frontend/widgets/results_table.dart';
import 'package:provider/provider.dart';

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
