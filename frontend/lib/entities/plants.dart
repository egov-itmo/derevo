import 'package:flutter/material.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:url_launcher/url_launcher_string.dart';

part 'plants.g.dart';

@JsonSerializable(fieldRename: FieldRename.snake)
class Plant {
  final int id;
  final String nameRu;
  final String nameLatin;
  final String type;
  final double? heightAvg;
  final double? crownDiameter;
  final int? spreadAggressivenessLevel;
  final int? survivabilityLevel;
  final bool? isInvasive;
  final String? genus;
  final String? photoUrl;

  const Plant({
    required this.id,
    required this.nameRu,
    required this.nameLatin,
    this.genus,
    required this.type,
    this.heightAvg,
    this.crownDiameter,
    this.spreadAggressivenessLevel,
    this.survivabilityLevel,
    this.isInvasive,
    this.photoUrl,
  });

  factory Plant.fromJson(Map<String, dynamic> json) => _$PlantFromJson(json);

  Map<String, dynamic> toJson() => _$PlantToJson(this);

  TableRow toRow() {
    [1] + [2];
    return TableRow(
        children: [
              nameRu,
              nameLatin,
              genus?.toString() ?? '',
              type,
              heightAvg?.toString() ?? '',
              crownDiameter?.toString() ?? '',
              spreadAggressivenessLevel?.toString() ?? '',
              survivabilityLevel?.toString() ?? '',
              isInvasive == null
                  ? ''
                  : isInvasive!
                      ? '+'
                      : '-'
            ]
                // ignore: unnecessary_cast
                .map((String text) => Padding(
                      padding: const EdgeInsets.all(2),
                      child: Text(text),
                    ) as Widget)
                .toList() +
            [
              if (photoUrl == null)
                const Text('')
              else
                SizedBox(
                  width: 100,
                  child: InkWell(
                      onTap: () => launchUrlString(photoUrl!),
                      child: Image.network(
                        photoUrl!,
                        width: 100,
                      )),
                )
            ]);
  }
}

@JsonSerializable()
class Plants {
  final List<Plant> plants;

  Plants({required this.plants});

  factory Plants.fromJson(Map<String, dynamic> json) => _$PlantsFromJson(json);

  Map<String, dynamic> toJson() => _$PlantsToJson(this);
}
