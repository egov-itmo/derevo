import 'package:flutter/material.dart';
import 'package:landscaping_frontend/models/compositions.dart';

class CompositionsModel extends ChangeNotifier {
  Compositions? _compositions;

  Compositions? get compositions => _compositions;

  set compositions(Compositions? newValue) {
    _compositions = newValue;
    notifyListeners();
  }
}
