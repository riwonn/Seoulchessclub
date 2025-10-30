import 'package:dio/dio.dart';
import '../models/meeting.dart';
import 'api_service.dart';

class MeetingService {
  final ApiService _apiService;

  MeetingService({required ApiService apiService}) : _apiService = apiService;

  /// 모든 모임 목록 조회
  Future<List<Meeting>> getAllMeetings() async {
    try {
      final response = await _apiService.get('/meetings');

      if (response.statusCode == 200) {
        final List<dynamic> data = response.data;
        return data.map((json) => Meeting.fromJson(json)).toList();
      } else {
        throw Exception('모임 목록 조회 실패');
      }
    } on DioException catch (e) {
      throw Exception('모임 목록 조회 중 오류가 발생했습니다: ${e.message}');
    }
  }

  /// 모임 참가 신청 (인증 필요)
  Future<Map<String, dynamic>> registerForMeeting(int meetingId) async {
    try {
      final response = await _apiService.post(
        '/meetings/register',
        queryParameters: {'meeting_id': meetingId},
      );

      if (response.statusCode == 201) {
        return response.data;
      } else {
        throw Exception('모임 참가 신청 실패');
      }
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw Exception('로그인이 필요합니다.');
      } else if (e.response?.statusCode == 403) {
        throw Exception('모임 정원이 초과되었습니다.');
      } else if (e.response?.statusCode == 409) {
        throw Exception('이미 참가 신청한 모임입니다.');
      }
      throw Exception('모임 참가 신청 중 오류가 발생했습니다: ${e.message}');
    }
  }

  /// 모임 관심 등록 (인증 필요)
  Future<Map<String, dynamic>> registerInterest(int meetingId) async {
    try {
      final response = await _apiService.post(
        '/meetings/register_interest',
        queryParameters: {'meeting_id': meetingId},
      );

      if (response.statusCode == 201) {
        return response.data;
      } else {
        throw Exception('모임 관심 등록 실패');
      }
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw Exception('로그인이 필요합니다.');
      } else if (e.response?.statusCode == 403) {
        throw Exception('모임 정원이 초과되었습니다.');
      } else if (e.response?.statusCode == 409) {
        throw Exception('이미 관심 등록한 모임입니다.');
      }
      throw Exception('모임 관심 등록 중 오류가 발생했습니다: ${e.message}');
    }
  }

  /// 모임 생성 (운영자용)
  Future<Meeting> createMeeting(MeetingCreate meetingData) async {
    try {
      final response = await _apiService.post(
        '/meetings/create',
        data: meetingData.toJson(),
      );

      if (response.statusCode == 201) {
        return Meeting.fromJson(response.data);
      } else {
        throw Exception('모임 생성 실패');
      }
    } on DioException catch (e) {
      throw Exception('모임 생성 중 오류가 발생했습니다: ${e.message}');
    }
  }
}

