import 'package:flutter/material.dart';
import 'package:latlong2/latlong.dart';

class MethodRequestModel extends ChangeNotifier {
  int? _humidityTypeId;
  int? _lightTypeId;
  int? _soilAcidityTypeId;
  int? _soilFertilityTypeId;
  int? _soilTypeId;

  List<LatLng> _polygon = [];
  List<int> _usedPlants = [];

  int? get humidityTypeId => _humidityTypeId;
  int? get lightTypeId => _lightTypeId;
  int? get soilAcidityTypeId => _soilAcidityTypeId;
  int? get soilFertilityTypeId => _soilFertilityTypeId;
  int? get soilTypeId => _soilTypeId;
  List<LatLng> get polygon => _polygon;
  List<int> get presentPlants => _usedPlants;

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

  void clearPresentPlants() {
    _usedPlants = [];
    notifyListeners();
  }

  void addPresentPlant(int plantId) {
    _usedPlants.add(plantId);
    notifyListeners();
  }

  void removePresentPlant(int plantId) {
    _usedPlants.remove(plantId);
    notifyListeners();
  }

  @override
  String toString() {
    return 'MethodRequestModel{humidityTypeId=$_humidityTypeId,'
        ' lightTypeId=$_lightTypeId, soilAcidityTypeId=$_soilAcidityTypeId,'
        ' soilFertilityTypeId=$_soilFertilityTypeId, soilTypeId=$_soilTypeId,'
        ' poligonPresent=${polygon.isNotEmpty}, presentPlants=$presentPlants}';
  }
}
