import 'package:json_annotation/json_annotation.dart';
import 'package:landscaping_frontend/models/plants.dart';

part 'compositions.g.dart';

@JsonSerializable(fieldRename: FieldRename.snake)
class Compositions {
  final List<Plants> compositions;

  Compositions({required this.compositions});

  factory Compositions.fromJson(Map<String, dynamic> json) =>
      _$CompositionsFromJson(json);

  Map<String, dynamic> toJson() => _$CompositionsToJson(this);
}
