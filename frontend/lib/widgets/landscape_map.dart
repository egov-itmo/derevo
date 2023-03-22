import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:positioned_tap_detector_2/positioned_tap_detector_2.dart';

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
  List<LatLng> tappedPoints = [];

  @override
  Widget build(BuildContext context) {
    final markers = tappedPoints.map((LatLng latlng) {
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

    Polygon? poly;
    if (tappedPoints.length > 2) {
      poly = Polygon(
        points: tappedPoints,
        isFilled: true,
        color: Colors.grey.withAlpha(180),
        borderColor: Colors.green,
      );
    }

    return FlutterMap(
      options: MapOptions(
        center: LatLng(59.95, 30.3),
        zoom: 10,
        onTap: _handleTap,
        onLongPress: (tapPosition, point) {
          setState(() {
            tappedPoints = [];
          });
        },
      ),
      children: [
        TileLayer(
          urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
          userAgentPackageName: 'org.kanootoko.landscaping_frontend',
        ),
        MarkerLayer(markers: markers),
        if (poly != null)
          PolygonLayer(
            polygons: [poly],
          )
      ],
    );
  }

  void _handleTap(TapPosition tapPosition, LatLng latlng) {
    setState(() {
      tappedPoints.add(latlng);
    });
  }
}
