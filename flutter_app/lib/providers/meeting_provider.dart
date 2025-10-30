import 'package:flutter/foundation.dart';
import '../models/meeting.dart';
import '../services/api_service.dart';
import '../services/meeting_service.dart';

class MeetingProvider with ChangeNotifier {
  final MeetingService _meetingService;
  
  List<Meeting> _meetings = [];
  bool _isLoading = false;
  String? _error;

  MeetingProvider({required ApiService apiService})
      : _meetingService = MeetingService(apiService: apiService);

  List<Meeting> get meetings => _meetings;
  bool get isLoading => _isLoading;
  String? get error => _error;

  /// 모임 목록 불러오기
  Future<void> fetchMeetings() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _meetings = await _meetingService.getAllMeetings();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// 모임 참가 신청
  Future<void> registerForMeeting(int meetingId) async {
    try {
      await _meetingService.registerForMeeting(meetingId);
      // 성공 후 모임 목록 새로고침
      await fetchMeetings();
    } catch (e) {
      rethrow;
    }
  }

  /// 모임 관심 등록
  Future<void> registerInterest(int meetingId) async {
    try {
      await _meetingService.registerInterest(meetingId);
      // 성공 후 모임 목록 새로고침
      await fetchMeetings();
    } catch (e) {
      rethrow;
    }
  }

  /// 모임 생성 (운영자용)
  Future<Meeting> createMeeting(MeetingCreate meetingData) async {
    try {
      final meeting = await _meetingService.createMeeting(meetingData);
      // 성공 후 모임 목록 새로고침
      await fetchMeetings();
      return meeting;
    } catch (e) {
      rethrow;
    }
  }

  /// ID로 모임 찾기
  Meeting? getMeetingById(int id) {
    try {
      return _meetings.firstWhere((meeting) => meeting.id == id);
    } catch (e) {
      return null;
    }
  }

  /// 참가 가능한 모임만 필터링
  List<Meeting> get availableMeetings {
    return _meetings.where((meeting) => meeting.isAvailable).toList();
  }

  /// 날짜순으로 정렬된 모임
  List<Meeting> get sortedMeetings {
    final sorted = List<Meeting>.from(_meetings);
    sorted.sort((a, b) => a.dateTime.compareTo(b.dateTime));
    return sorted;
  }
}

