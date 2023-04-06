import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:landscaping_frontend/models/limitations_response.dart';
import 'package:latlong2/latlong.dart';
import 'package:positioned_tap_detector_2/positioned_tap_detector_2.dart';

import 'package:landscaping_frontend/models/method_request.dart';
import 'package:provider/provider.dart';

class LandscapeMap extends StatefulWidget {
  const LandscapeMap({
    super.key,
  });

  @override
  State<LandscapeMap> createState() => _LandscapeMapState();
}

enum CurrentAction {
  noAction,
  addPoint,
  startAgain,
}

class _LandscapeMapState extends State<LandscapeMap> {
  CurrentAction currentAction = CurrentAction.addPoint;

  @override
  Widget build(BuildContext context) {
    var request = context.watch<MethodRequestModel>();
    var limitations = context.watch<LimitationsResponseModel>();

    final markers = request.polygon.map((LatLng latlng) {
      return Marker(
        width: 50,
        height: 50,
        point: latlng,
        builder: (ctx) => GestureDetector(
          onLongPress: () {
            debugPrint("test!");
            // for (LatLng point in tappedPoints) {
            //   if (point == latlng) {
            //     setState(() {
            //       tappedPoints.remove(point);
            //     });
            //     break;
            //   }
            // }
            // debugPrint("I was here");
          },
          child: const Icon(Icons.circle, color: Colors.red),
        ),
      );
    }).toList();

    Polygon? selectionPolygon;
    if (markers.length > 2) {
      selectionPolygon = Polygon(
        points: request.polygon,
        isFilled: true,
        color: Colors.green.withAlpha(180),
        borderColor: Colors.green,
      );
    }

    return FlutterMap(
      options: MapOptions(
        center: LatLng(59.95, 30.3),
        zoom: 10,
        onTap: (tapPosition, point) =>
            _handleTap(tapPosition, point, request.polygon),
        onLongPress: (tapPosition, point) {
          setState(() {
            if (request.polygon.isNotEmpty) {
              request.polygon.removeLast();
            }
          });
        },
      ),
      children: [
        TileLayer(
          urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
          userAgentPackageName: 'org.kanootoko.landscaping_frontend',
        ),
        MarkerLayer(markers: markers),
        if (selectionPolygon != null)
          PolygonLayer(
            polygons: [selectionPolygon],
          ),
        if (limitations.limitationFactors != null)
          PolygonLayer(polygons: limitations.limitationFactors!),
      ],
    );
  }

  void _handleTap(
      TapPosition tapPosition, LatLng latlng, List<LatLng> polygon) {
    setState(() {
      polygon.add(latlng);
    });
  }
}
