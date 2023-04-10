import 'package:flutter/material.dart';
import 'package:latlong2/latlong.dart';

class MethodRequestModel extends ChangeNotifier {
  int? _humidityTypeId;
  int? _lightTypeId;
  int? _soilAcidityTypeId;
  int? _soilFertilityTypeId;
  int? _soilTypeId;

  List<LatLng> _polygon = [];

  int? get humidityTypeId => _humidityTypeId;
  int? get lightTypeId => _lightTypeId;
  int? get soilAcidityTypeId => _soilAcidityTypeId;
  int? get soilFertilityTypeId => _soilFertilityTypeId;
  int? get soilTypeId => _soilTypeId;
  List<LatLng> get polygon => _polygon;

  set humidityTypeId(int? newValue) {
    _humidityTypeId = newValue;
    notifyListeners();
  }

  set lightTypeId(int? newValue) {
    _lightTypeId = newValue;
    notifyListeners();
  }

  set soilAcidityTypeId(int? newValue) {
    _soilAcidityTypeId = newValue;
    notifyListeners();
  }

  set soilFertilityTypeId(int? newValue) {
    _soilFertilityTypeId = newValue;
    notifyListeners();
  }

  set soilTypeId(int? newValue) {
    _soilTypeId = newValue;
    notifyListeners();
  }

  set polygon(List<LatLng> newValue) {
    _polygon = newValue;
    notifyListeners();
  }

  @override
  String toString() {
    return 'MethodRequestModel{humidityTypeId=$_humidityTypeId,'
        ' lightTypeId=$_lightTypeId, soilAcidityTypeId=$_soilAcidityTypeId,'
        ' soilFertilityTypeId=$_soilFertilityTypeId, soilTypeId=$_soilTypeId,'
        ' poligonPresent=${polygon.isNotEmpty}}';
  }
}

// import 'package:flutter/material.dart';
// import 'package:latlong2/latlong.dart';

// class MethodRequestModel extends InheritedWidget {
//   final int? humidityTypeId;
//   final int? lightTypeId;
//   final int? soilAcidityTypeId;
//   final int? soilFertilityTypeId;
//   final int? soilTypeId;
//   final List<LatLng> polygon;

//   const MethodRequestModel({
//     super.key,
//     this.humidityTypeId,
//     this.lightTypeId,
//     this.soilAcidityTypeId,
//     this.soilFertilityTypeId,
//     this.soilTypeId,
//     this.polygon = const [],
//     required super.child,
//   });

//   static MethodRequestModel? maybeOf(BuildContext context) {
//     return context.dependOnInheritedWidgetOfExactType<MethodRequestModel>();
//   }

//   static MethodRequestModel of(BuildContext context) {
//     final MethodRequestModel? result = maybeOf(context);
//     assert(result != null, 'No MethodRequestModel found in context');
//     return result!;
//   }

//   @override
//   bool updateShouldNotify(MethodRequestModel oldWidget) => true;
// }
