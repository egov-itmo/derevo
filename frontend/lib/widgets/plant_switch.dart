import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/method_request.dart';

class PlantSwitch extends StatelessWidget {
  final int plantId;
  const PlantSwitch(this.plantId, {super.key});

  @override
  Widget build(BuildContext context) {
    var request = context.watch<MethodRequestModel>();
    if (request.presentPlants.contains(plantId)) {
      return IconButton(
        icon: const Icon(
          Icons.add_box,
          color: Colors.green,
        ),
        onPressed: () => request.removePresentPlant(plantId),
      );
    } else {
      return IconButton(
        icon: const Icon(Icons.add_box_outlined),
        onPressed: () => request.addPresentPlant(plantId),
      );
    }
  }
}
