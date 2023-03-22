import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:landscaping_frontend/entities/limitation_factors.dart';
import 'package:landscaping_frontend/config/config.dart';

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

  const NameAndSelect(
      {required this.limitationFactorName, required this.select});
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
                  onPressed: _callBackend,
                  child: const Text("Использовать заданный полигон"),
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                      backgroundColor: widget.theme.colorScheme.primary,
                      foregroundColor: widget.theme.colorScheme.onPrimary),
                  child: const Text("Подобрать породный состав"),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _callBackend() {}
}

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
  static const String _uncheckedText = 'Не выбрано';
  String _current = _uncheckedText;

  _LimitationFactorSelectState();

  @override
  void initState() {
    super.initState();
    futureLimitationFactors = _fetch();
  }

  Future<int?> checkedId() async {
    if (_current == _uncheckedText) {
      return null;
    }
    for (LimitationFactor limitationFactor
        in (await futureLimitationFactors).values) {
      if (_current == limitationFactor.name) {
        return limitationFactor.id;
      }
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    ThemeData theme = Theme.of(context);
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
      return LimitationFactors.fromJson(
          jsonDecode(utf8.decode(response.bodyBytes)));
    } else {
      throw Exception('Ошибка загрузки');
    }
  }
}
