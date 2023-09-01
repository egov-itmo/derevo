import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:landscaping_frontend/config/config.dart';
import 'package:landscaping_frontend/models/plants.dart';
import 'package:landscaping_frontend/widgets/plant_switch.dart';

class PlantsListPage extends StatefulWidget {
  const PlantsListPage({super.key});

  @override
  State<PlantsListPage> createState() => _PlantsListPageState();
}

class _PlantsListPageState extends State<PlantsListPage> {
  late Future<Plants> futurePlants;

  @override
  void initState() {
    super.initState();
    futurePlants = _fetch();
  }

  @override
  Widget build(BuildContext context) {
    var theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.all(8),
      child: FutureBuilder<Plants>(
          future: futurePlants,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              return Column(
                children: [
                  const SizedBox(
                    width: 1200,
                    child: Padding(
                      padding: EdgeInsets.all(8.0),
                      child: Text(
                        "Таблица включает в себя список подобранных растений и"
                        " содержит описание некоторых основных характеристик для"
                        " каждого вида, которые являются вспомогательными для"
                        " понимания расположения на местности и корректировки"
                        "количества применения единиц растений.\n"
                        'В столбце "Наличие" можно отметить виды растений, '
                        " которые уже присутствуют в заданной области.",
                        style: TextStyle(fontSize: 18),
                      ),
                    ),
                  ),
                  Expanded(child: PlantsTable(snapshot.data!.plants)),
                ],
              );
            } else if (snapshot.hasError) {
              return Text(
                '${snapshot.error}',
                style: TextStyle(color: theme.colorScheme.error),
              );
            }
            return const CircularProgressIndicator();
          }),
    );
  }

  Future<Plants> _fetch() async {
    final response =
        await http.get(Uri.parse('${appConfig.apiHost}/api/plants/all'));

    if (response.statusCode == 200) {
      return Plants.fromJson(jsonDecode(utf8.decode(response.bodyBytes)));
    } else {
      throw Exception('Ошибка загрузки (${response.statusCode})');
    }
  }
}

class PlantsTable extends StatelessWidget {
  final List<Plant> plants;
  final bool withSwitch;

  const PlantsTable(this.plants, {super.key, this.withSwitch = true});

  @override
  Widget build(BuildContext context) {
    var widths = withSwitch
        ? const {
            0: FixedColumnWidth(70),
            1: FixedColumnWidth(180),
            2: FixedColumnWidth(160),
            3: FixedColumnWidth(120),
            4: FixedColumnWidth(120),
            5: FixedColumnWidth(80),
            6: FixedColumnWidth(80),
            7: FixedColumnWidth(110),
            8: FixedColumnWidth(115),
            9: FixedColumnWidth(105),
            10: FixedColumnWidth(102),
          }
        : const {
            0: FixedColumnWidth(180),
            1: FixedColumnWidth(160),
            2: FixedColumnWidth(120),
            3: FixedColumnWidth(120),
            4: FixedColumnWidth(80),
            5: FixedColumnWidth(80),
            6: FixedColumnWidth(110),
            7: FixedColumnWidth(115),
            8: FixedColumnWidth(105),
            9: FixedColumnWidth(102),
          };
    return SingleChildScrollView(
      scrollDirection: Axis.vertical,
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Table(
          border: TableBorder.all(),
          columnWidths: widths,
          children: [
            TableRow(
              children: [
                if (withSwitch) "Наличие",
                "Название",
                "Латинское название",
                "Род",
                "Тип",
                "Высота",
                "Размер кроны",
                "Агрессивность",
                "Выживаемость",
                "Инвазивность",
                "Фото",
              ]
                  .map(
                    (String text) => Padding(
                      padding: const EdgeInsets.all(2),
                      child: Center(
                        child: Text(
                          text,
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                  )
                  .toList(),
            ),
            for (Plant plant in plants)
              plant.toRow(
                  firstWidget: withSwitch ? PlantSwitch(plant.id) : null)
          ],
        ),
      ),
    );
  }
}
