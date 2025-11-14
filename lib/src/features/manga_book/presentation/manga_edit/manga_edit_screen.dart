// Copyright (c) 2022 Contributors to the Suwayomi project
//
// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

import '../../data/manga_book/manga_book_repository.dart';
import '../../domain/manga/manga_model.dart';
import '../../../../graphql/__generated__/schema.graphql.dart';

class MangaEditScreen extends HookConsumerWidget {
  const MangaEditScreen({super.key, required this.manga});
  final MangaDto manga;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final formKey = useMemoized(() => GlobalKey<FormState>());
    final titleController = useTextEditingController(text: manga.title);
    final genreController = useTextEditingController(text: manga.genre.join(', '));
    final mangaBookRepository = ref.watch(mangaBookRepositoryProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Edit Manga'),
        actions: [
          IconButton(
            onPressed: () async {
              if (formKey.currentState!.validate()) {
                final genres = genreController.text
                    .split(',')
                    .map((e) => e.trim())
                    .toList();

                await mangaBookRepository.client.mutate$UpdateManga(
                  Options$Mutation$UpdateManga(
                    variables: Variables$Mutation$UpdateManga(
                      input: Input$UpdateMangaInput(
                        id: manga.id,
                        patch: Input$UpdateMangaPatchInput(
                          title: titleController.text,
                          genre: genres,
                        ),
                      ),
                    ),
                  ),
                );

                Navigator.of(context).pop(true);
              }
            },
            icon: const Icon(Icons.save),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: formKey,
          child: Column(
            children: [
              TextFormField(
                controller: titleController,
                decoration: const InputDecoration(
                  labelText: 'Title',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter a title';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16.0),
              TextFormField(
                controller: genreController,
                decoration: const InputDecoration(
                  labelText: 'Genres',
                  border: OutlineInputBorder(),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
