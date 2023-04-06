import 'dart:io';
import 'package:flutter/services.dart';
import 'package:landscaping_frontend/config/config.dart';
import 'package:landscaping_frontend/models/limitations_response.dart';
import 'package:provider/provider.dart';
import 'package:yaml/yaml.dart';
import 'package:flutter/material.dart';
import 'package:landscaping_frontend/widgets/choose_options.dart';
import 'package:landscaping_frontend/widgets/landscape_map.dart';
import 'package:landscaping_frontend/models/method_request.dart';

final HttpClient httpClient = HttpClient();

Future<void> main() async {
  final yamlString = await rootBundle.loadString('assets/my_config.yaml');
  final dynamic yamlMap = loadYaml(yamlString);

  appConfig.apiHost = yamlMap['api_host'] ?? appConfig.apiHost;

  runApp(MultiProvider(
    providers: [
      ChangeNotifierProvider(create: (context) => MethodRequestModel()),
      ChangeNotifierProvider(create: (context) => LimitationsResponseModel())
    ],
    child: const LandscapingFrontendApp(),
  ));
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
