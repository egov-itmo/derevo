import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:landscaping_frontend/config/config.dart';
import 'package:landscaping_frontend/models/limitation_factors.dart';
import 'package:landscaping_frontend/notifiers/method_request.dart';
import 'package:provider/provider.dart';

class LimitationFactorSelect extends StatefulWidget {
  final LimitationFactorType limitationFactorType;

  const LimitationFactorSelect(
    this.limitationFactorType, {
    super.key,
  });

  @override
  State<LimitationFactorSelect> createState() => _LimitationFactorSelectState();
}

class _LimitationFactorSelectState extends State<LimitationFactorSelect> {
  late Future<LimitationFactors> futureLimitationFactors;
  final Map<String, int> _nameIdMapping = {};
  static const String _uncheckedText = 'Не выбрано';
  String _current = _uncheckedText;

  _LimitationFactorSelectState();

  @override
  void initState() {
    super.initState();
    futureLimitationFactors = _fetch();
  }

  int? checkedId() {
    if (_current == _uncheckedText) {
      return null;
    }
    if (_nameIdMapping.containsKey(_current)) {
      return _nameIdMapping[_current];
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    ThemeData theme = Theme.of(context);
    var request = context.watch<MethodRequestModel>();

    return FutureBuilder<LimitationFactors>(
      future: futureLimitationFactors,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return DropdownButton<String>(
            value: _current,
            items: [
              _uncheckedText,
              for (LimitationFactor limitationFactor in snapshot.data!.values)
                limitationFactor.name
            ].map((String value) {
              return DropdownMenuItem<String>(
                value: value,
                child: Text(value),
              );
            }).toList(),
            onChanged: (String? newValue) {
              setState(() {
                _current = newValue ?? _uncheckedText;
                if (widget.limitationFactorType ==
                    LimitationFactorType.humidityType) {
                  request.humidityTypeId = checkedId();
                } else if (widget.limitationFactorType ==
                    LimitationFactorType.lightType) {
                  request.lightTypeId = checkedId();
                } else if (widget.limitationFactorType ==
                    LimitationFactorType.soilAcidityType) {
                  request.soilAcidityTypeId = checkedId();
                } else if (widget.limitationFactorType ==
                    LimitationFactorType.soilFertilityType) {
                  request.soilFertilityTypeId = checkedId();
                } else if (widget.limitationFactorType ==
                    LimitationFactorType.soilType) {
                  request.soilTypeId = checkedId();
                }
              });
            },
          );
        } else if (snapshot.hasError) {
          return Text(
            '${snapshot.error}',
            style: TextStyle(color: theme.colorScheme.error),
          );
        }
        return const CircularProgressIndicator();
      },
    );
  }

  Future<LimitationFactors> _fetch() async {
    final response = await http.get(Uri.parse(
        '${appConfig.apiHost}${limitationFactorEndpoints[widget.limitationFactorType]}'));

    if (response.statusCode == 200) {
      var limitationFactors = LimitationFactors.fromJson(
          jsonDecode(utf8.decode(response.bodyBytes)));
      for (LimitationFactor limitationFactor in limitationFactors.values) {
        _nameIdMapping[limitationFactor.name] = limitationFactor.id;
      }
      return limitationFactors;
    } else {
      throw Exception('Ошибка загрузки');
    }
  }
}
