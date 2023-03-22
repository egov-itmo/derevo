import 'dart:io';

import 'package:flutter/material.dart';
import 'package:landscaping_frontend/widgets/choose_options.dart';
import 'package:landscaping_frontend/widgets/landscape_map.dart';

const String apiHost = "http://localhost:8080";

final HttpClient httpClient = HttpClient();

void main() {
  runApp(const LandscapingFrontendApp());
}

class LandscapingFrontendApp extends StatelessWidget {
  const LandscapingFrontendApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Landscaping Frontend App',
      theme: ThemeData(
        colorSchemeSeed: Colors.green[800],
        scaffoldBackgroundColor: Colors.green[100],
        useMaterial3: true,
      ),
      home: const LandscapingHome(),
    );
  }
}

class LandscapingHome extends StatelessWidget {
  const LandscapingHome({super.key});

  @override
  Widget build(BuildContext context) {
    ThemeData theme = Theme.of(context);
    return Scaffold(
      body: Stack(
        children: [
          const LandscapeMap(),
          Positioned(
            right: 40,
            top: 40,
            width: 300,
            child: ChooseOptions(theme: theme),
          ),
        ],
      ),
    );
  }
}
