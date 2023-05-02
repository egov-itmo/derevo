import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:geojson_vi/geojson_vi.dart';
import 'package:http/http.dart' as http;
import 'package:landscaping_frontend/config/config.dart';
import 'package:landscaping_frontend/entities/limitation_factors.dart';
import 'package:landscaping_frontend/models/limitations_response.dart';
import 'package:landscaping_frontend/models/method_request.dart';
import 'package:latlong2/latlong.dart';
import 'package:provider/provider.dart';

import 'limitation_factors_select_state.dart';

class ChooseOptions extends StatefulWidget {
  const ChooseOptions({
    super.key,
    required this.theme,
  });

  final ThemeData theme;

  @override
  State<ChooseOptions> createState() => _ChooseOptionsState();
}

class NameAndSelect {
  final String limitationFactorName;
  final LimitationFactorSelect select;

  const NameAndSelect({
    required this.limitationFactorName,
    required this.select,
  });
}

class _ChooseOptionsState extends State<ChooseOptions> {
  final List<NameAndSelect> limitationFactors = const [
    NameAndSelect(
      limitationFactorName: "тип освещенности",
      select: LimitationFactorSelect(LimitationFactorType.lightType),
    ),
    NameAndSelect(
      limitationFactorName: "тип влажности воздуха",
      select: LimitationFactorSelect(LimitationFactorType.humidityType),
    ),
    NameAndSelect(
      limitationFactorName: "тип кислотности почвы",
      select: LimitationFactorSelect(LimitationFactorType.soilAcidityType),
    ),
    NameAndSelect(
      limitationFactorName: "тип плодородности почвы",
      select: LimitationFactorSelect(LimitationFactorType.soilFertilityType),
    ),
    NameAndSelect(
      limitationFactorName: "тип почвы",
      select: LimitationFactorSelect(LimitationFactorType.soilType),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    List<Widget> selects = [];
    var limitations = context.watch<LimitationsResponseModel>();
    var request = context.watch<MethodRequestModel>();

    for (NameAndSelect nameAndSelect in limitationFactors) {
      selects.add(Text("Выберите ${nameAndSelect.limitationFactorName}"));
      selects.add(nameAndSelect.select);
      selects.add(const SizedBox(height: 20));
    }
    return ColoredBox(
      color: Colors.green.shade50,
      child: Align(
        alignment: Alignment.topLeft,
        child: Form(
          child: Padding(
            padding: const EdgeInsets.all(12.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ...selects,
                ElevatedButton(
                    onPressed: () {
                      request.polygon.clear();
                      limitations.limitationFactors = null;
                    },
                    child: const Text("Очистить")),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: () async =>
                      await _callGetLimitations(limitations, request.polygon),
                  child: const Text("Просмотр факторов"),
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: () => _callMethodCalculation(request),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: widget.theme.colorScheme.primary,
                    foregroundColor: widget.theme.colorScheme.onPrimary,
                  ),
                  child: const Text("Подобрать породный состав"),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Future<void> _callGetLimitations(
      LimitationsResponseModel limitations, List<LatLng> polygon) async {
    if (polygon.length < 3) {
      return;
    }
    final Map<String, Color> limitationFactorColors = {
      "Устойчивость к засолению": Colors.yellow.shade300.withAlpha(130),
      "Устойчивость к пересыханию": Colors.yellowAccent.withAlpha(130),
      "Устойчивость к подтоплению": Colors.blue.shade800.withAlpha(130),
      "Газостойкость": Colors.blue.shade200.withAlpha(130),
      "Ветроустойчивость": Colors.teal.shade200.withAlpha(130),
    };

    String polygonAsBody = jsonEncode({
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            for (var latlng in polygon) [latlng.longitude, latlng.latitude]
          ],
        ],
      },
    });
    var response = await http.post(
      Uri.parse("${appConfig.apiHost}/api/limitations/limitation_factors"),
      headers: {"Content-Type": "application/json"},
      body: polygonAsBody,
    );
    if (response.statusCode == 200) {
      var geoJsonText = utf8.decode(response.bodyBytes);

      var geo = GeoJSONFeatureCollection.fromJSON(geoJsonText);

      List<Polygon> polygons = [];
      for (var feature in geo.features) {
        if (feature!.geometry.type == GeoJSONType.polygon) {
          var geom = feature.geometry.toMap()["coordinates"][0];
          var points = <LatLng>[
            for (var entry in geom) LatLng(entry[1], entry[0])
          ];
          polygons.add(
            Polygon(
                points: points,
                color: limitationFactorColors[
                        feature.properties?["name"] ?? "default"] ??
                    Colors.blueGrey.withAlpha(130),
                isFilled: true),
          );
        }
      }
      limitations.limitationFactors = polygons;
      debugPrint("Got ${polygons.length} limitation factors");
    } else {
      debugPrint("Got error code: ${response.statusCode}");
    }
  }

  void _callMethodCalculation(MethodRequestModel request) {
    debugPrint('Requesting backend with $request');
  }
}
