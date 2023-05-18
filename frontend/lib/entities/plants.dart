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
  final String? thumbnailUrl;

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
    this.thumbnailUrl,
  });

  factory Plant.fromJson(Map<String, dynamic> json) => _$PlantFromJson(json);

  Map<String, dynamic> toJson() => _$PlantToJson(this);

  TableRow toRow({Widget? firstWidget}) {
    return TableRow(children: [
      if (firstWidget != null) firstWidget,
      Padding(
        padding: const EdgeInsets.all(2),
        child: Text(nameRu),
      ),
      Padding(
        padding: const EdgeInsets.all(2),
        child: Text(nameLatin),
      ),
      (genus?.toString() ?? '') != ''
          ? Padding(
              padding: const EdgeInsets.all(2),
              child: Text(genus!.toString()),
            )
          : const SizedBox(),
      Padding(
        padding: const EdgeInsets.all(2),
        child: Text(type),
      ),
      (heightAvg?.toString() ?? '') != ''
          ? Padding(
              padding: const EdgeInsets.all(2),
              child: Text(heightAvg!.toString()),
            )
          : const SizedBox(),
      (crownDiameter?.toString() ?? '') != ''
          ? Padding(
              padding: const EdgeInsets.all(2),
              child: Text(crownDiameter!.toString()),
            )
          : const SizedBox(),
      (spreadAggressivenessLevel?.toString() ?? '') != ''
          ? Padding(
              padding: const EdgeInsets.all(2),
              child: Text(spreadAggressivenessLevel!.toString()),
            )
          : const SizedBox(),
      (survivabilityLevel?.toString() ?? '') != ''
          ? Padding(
              padding: const EdgeInsets.all(2),
              child: Text(survivabilityLevel!.toString()),
            )
          : const SizedBox(),
      isInvasive == null
          ? const SizedBox()
          : isInvasive!
              ? const Icon(Icons.add)
              : const Icon(Icons.remove),
      if (photoUrl == null)
        const Text('')
      else
        SizedBox(
          width: 100,
          child: InkWell(
              onTap: () => launchUrlString(photoUrl!),
              child: Image.network(thumbnailUrl!)),
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
