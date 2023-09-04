import 'dart:io';

import 'package:flutter/material.dart';
import 'package:global_configuration/global_configuration.dart';
import 'package:landscaping_frontend/config/config.dart';
import 'package:landscaping_frontend/notifiers/compositions.dart';
import 'package:landscaping_frontend/notifiers/limitations_response.dart';
import 'package:landscaping_frontend/notifiers/method_request.dart';
import 'package:landscaping_frontend/pages/map.dart';
import 'package:landscaping_frontend/pages/plants_list.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher_string.dart';

final HttpClient httpClient = HttpClient();

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await GlobalConfiguration().loadFromAsset("config.json");
  appConfig.apiHost = GlobalConfiguration().getValue("api_host");

  runApp(MultiProvider(
    providers: [
      ChangeNotifierProvider(create: (context) => MethodRequestModel()),
      ChangeNotifierProvider(create: (context) => LimitationsResponseModel()),
      ChangeNotifierProvider(create: (context) => CompositionsModel()),
    ],
    child: const LandscapingFrontendApp(),
  ));
}

class LandscapingFrontendApp extends StatelessWidget {
  const LandscapingFrontendApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'Генерация композиций растений',
        theme: ThemeData(
          colorSchemeSeed: Colors.green[800],
          scaffoldBackgroundColor: Colors.green[100],
          useMaterial3: true,
        ),
        home: const Headered(child: MapPage()),
        routes: {
          '/plants': (BuildContext context) =>
              const Headered(child: PlantsListPage()),
        });
  }
}

class Headered extends StatelessWidget {
  final Widget child;

  const Headered({
    required this.child,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    var theme = Theme.of(context);
    return Scaffold(
      body: Column(children: [
        SizedBox(
          child: Container(
            height: 40,
            padding: const EdgeInsets.all(2.0),
            color: theme.primaryColor,
            alignment: Alignment.center,
            child: Row(children: [
              ElevatedButton(
                onPressed: () {
                  var current =
                      ModalRoute.of(context)?.settings.name ?? "unknown";
                  if (current == '/plants' && Navigator.canPop(context)) {
                    Navigator.pop(context);
                  } else if (current != '/') {
                    Navigator.pushNamed(context, '/');
                  }
                },
                child: const Text("Карта"),
              ),
              const SizedBox(width: 10),
              ElevatedButton(
                onPressed: () {
                  if (ModalRoute.of(context)?.settings.name != 'plants') {
                    Navigator.pushNamed(context, '/plants');
                  }
                },
                child: const Text("Список растений"),
              ),
              Expanded(child: Container()),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: InkWell(
                    child: Text(
                      "О системе",
                      style: TextStyle(
                          color: Colors.blue.shade500,
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                          decoration: TextDecoration.underline),
                    ),
                    onTap: () => launchUrlString(
                        "https://news.egov.itmo.ru/map/dev/index.html")),
              ),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: InkWell(
                  child: const Icon(Icons.info_outline_rounded),
                  onTap: () => launchUrlString(
                      "https://news.egov.itmo.ru/map/dev/index.html#info"),
                ),
              )
            ]),
          ),
        ),
        Expanded(child: child),
      ]),
    );
  }
}
