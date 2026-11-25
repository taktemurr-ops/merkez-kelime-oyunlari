import 'package:flutter/material.dart';
import 'package:studio_core/app/approved_hub.dart';

/// Onaylı tasarım (Oyun Merkezleri · Tasarım Örnekleri).
const approvedStyle = ApprovedHubStyle(
  background: [Color(0xFF5A2AB0), Color(0xFF34187A), Color(0xFF170C44)],
  accent: Color(0xFFFF5BC8),
  card: Color(0xFF6A34C4),
  play: Color(0xFF1FA2F2),
  number: Color(0xFFFF6BD0),
  heroAsset: 'assets/approved/hero.png',
  heroTitle: true,
  blocks: [ApprovedBlock.search, ApprovedBlock.featured],
  featuredKey: 'featured',
  featured: ['oyun-kelime-avi', 'oyun-cengel-bulmaca', 'oyun-adam-asmaca', 'oyun-ters-kelime-anagram-yarisi'],
  tileArt: {
    'oyun-kelime-avi': 'assets/approved/tile_arama.png',
    'oyun-cengel-bulmaca': 'assets/approved/tile_capraz.png',
    'oyun-adam-asmaca': 'assets/approved/tile_asmaca.png',
    'oyun-ters-kelime-anagram-yarisi': 'assets/approved/tile_harf.png',
  },
  tilesPerPage: 4,
);
