import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Semantic Search',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF6C63FF),
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        textTheme: GoogleFonts.outfitTextTheme(),
      ),
      home: const SemanticSearchPage(),
    );
  }
}

// Data Model
class SearchResult {
  final String id;
  final String context;
  final double score;

  SearchResult({
    required this.id,
    required this.context,
    required this.score,
  });

  factory SearchResult.fromJson(Map<String, dynamic> json) {
    return SearchResult(
      id: json['id'] ?? '',
      context: json['context'] ?? '',
      score: (json['score'] as num).toDouble(),
    );
  }
}

// API Service
class SearchService {
  static const String baseUrl =
      '';

  Future<List<SearchResult>> search(String query) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/search'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'query': query,
          'top_k': 10,
          'index_name': 'embedding-search',
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final List<dynamic> matches = data['matches'];
        return matches.map((json) => SearchResult.fromJson(json)).toList();
      } else {
        print(response.body);
        throw Exception('Failed to load search results');
      }
    } catch (e) {
      print(e);
      throw Exception('Error searching: $e');
    }
  }
}

class SemanticSearchPage extends StatefulWidget {
  const SemanticSearchPage({super.key});

  @override
  State<SemanticSearchPage> createState() => _SemanticSearchPageState();
}

class _SemanticSearchPageState extends State<SemanticSearchPage> {
  final TextEditingController _searchController = TextEditingController();
  final SearchService _searchService = SearchService();
  List<SearchResult> _results = [];
  bool _isLoading = false;
  String? _error;

  Future<void> _performSearch(String query) async {
    if (query.isEmpty) return;

    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final results = await _searchService.search(query);
      setState(() {
        _results = results;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F5F7),
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const HeaderWidget(),
            SearchBarWidget(
              controller: _searchController,
              onSubmitted: _performSearch,
            ),
            Expanded(
              child: ResultsListWidget(
                isLoading: _isLoading,
                error: _error,
                results: _results,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class HeaderWidget extends StatelessWidget {
  const HeaderWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Discover',
            style: GoogleFonts.outfit(
              fontSize: 32,
              fontWeight: FontWeight.bold,
              color: const Color(0xFF1A1A1A),
            ),
          ).animate().fadeIn().slideX(),
          const SizedBox(height: 8),
          Text(
            'Semantic search powered by AI',
            style: GoogleFonts.outfit(
              fontSize: 16,
              color: const Color(0xFF666666),
            ),
          ).animate().fadeIn(delay: 200.ms).slideX(),
        ],
      ),
    );
  }
}

class SearchBarWidget extends StatelessWidget {
  final TextEditingController controller;
  final Function(String) onSubmitted;

  const SearchBarWidget({
    super.key,
    required this.controller,
    required this.onSubmitted,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 8.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 20,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: TextField(
        controller: controller,
        onSubmitted: onSubmitted,
        style: GoogleFonts.outfit(fontSize: 16),
        decoration: InputDecoration(
          hintText: 'Search for anything...',
          hintStyle: GoogleFonts.outfit(color: const Color(0xFF999999)),
          prefixIcon: const Icon(Icons.search, color: Color(0xFF6C63FF)),
          suffixIcon: IconButton(
            icon: const Icon(Icons.arrow_forward_rounded,
                color: Color(0xFF6C63FF)),
            onPressed: () => onSubmitted(controller.text),
          ),
          border: InputBorder.none,
          contentPadding: const EdgeInsets.all(20),
        ),
      ),
    ).animate().fadeIn(delay: 400.ms).slideY(begin: 0.2);
  }
}

class ResultsListWidget extends StatelessWidget {
  final bool isLoading;
  final String? error;
  final List<SearchResult> results;

  const ResultsListWidget({
    super.key,
    required this.isLoading,
    this.error,
    required this.results,
  });

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Center(
        child: CircularProgressIndicator(
          color: Color(0xFF6C63FF),
        ),
      );
    }

    if (error != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Text(
            error!,
            style: GoogleFonts.outfit(color: Colors.red),
            textAlign: TextAlign.center,
          ),
        ),
      );
    }

    if (results.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.article_outlined, size: 64, color: Colors.grey[300]),
            const SizedBox(height: 16),
            Text(
              'Start searching to see results',
              style: GoogleFonts.outfit(
                fontSize: 16,
                color: Colors.grey[400],
              ),
            ),
          ],
        ),
      ).animate().fadeIn(delay: 600.ms);
    }

    return ListView.builder(
      padding: const EdgeInsets.all(24),
      itemCount: results.length,
      itemBuilder: (context, index) {
        final result = results[index];
        final isTopMatch = index == 0;

        return ResultCardWidget(
          result: result,
          index: index,
          isTopMatch: isTopMatch,
        );
      },
    );
  }
}

class ResultCardWidget extends StatelessWidget {
  final SearchResult result;
  final int index;
  final bool isTopMatch;

  const ResultCardWidget({
    super.key,
    required this.result,
    required this.index,
    required this.isTopMatch,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: isTopMatch
            ? Border.all(
                color: const Color(0xFF6C63FF).withOpacity(0.3), width: 2)
            : null,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.03),
            blurRadius: 15,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: isTopMatch
                        ? const Color(0xFF6C63FF)
                        : const Color(0xFFF0F0F0),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    '${(result.score * 100).toStringAsFixed(1)}% Match',
                    style: GoogleFonts.outfit(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: isTopMatch ? Colors.white : Colors.black54,
                    ),
                  ),
                ),
                if (isTopMatch)
                  const Icon(Icons.star_rounded,
                      color: Color(0xFFFFD700), size: 20),
              ],
            ),
            const SizedBox(height: 16),
            Text(
              result.context,
              style: GoogleFonts.outfit(
                fontSize: 16,
                height: 1.5,
                color: const Color(0xFF2D2D2D),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Icon(Icons.tag, size: 14, color: Colors.grey[400]),
                const SizedBox(width: 4),
                Text(
                  'ID: ${result.id}',
                  style: GoogleFonts.outfit(
                    fontSize: 12,
                    color: Colors.grey[400],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    )
        .animate()
        .fadeIn(delay: (100 * index).ms)
        .slideY(begin: 0.2, curve: Curves.easeOutQuad);
  }
}
