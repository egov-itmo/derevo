import 'package:flutter/material.dart';
import 'package:landscaping_frontend/widgets/choose_options.dart';
import 'package:landscaping_frontend/widgets/landscape_map.dart';

class MapPage extends StatelessWidget {
  const MapPage({super.key});

  @override
  Widget build(BuildContext context) {
    ThemeData theme = Theme.of(context);
    return Stack(
      children: [
        const LandscapeMap(),
        Positioned(
          right: 40,
          top: 40,
          width: 300,
          child: ChooseOptions(theme: theme),
        ),
      ],
    );
  }
}
