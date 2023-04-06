import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';

class LimitationsResponseModel extends ChangeNotifier {
  List<Polygon>? _limitationFactors;
  List<Polygon>? _lightFactors;

  List<Polygon>? get limitationFactors => _limitationFactors;
  List<Polygon>? get lightFactors => _lightFactors;

  set limitationFactors(List<Polygon>? newValue) {
    _limitationFactors = newValue;
    notifyListeners();
  }

  set lightFactors(List<Polygon>? newValue) {
    _lightFactors = newValue;
    notifyListeners();
  }

  void ready() {}
}
