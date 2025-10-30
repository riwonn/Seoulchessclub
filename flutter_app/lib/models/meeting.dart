import 'package:json_annotation/json_annotation.dart';
import 'user.dart';

part 'meeting.g.dart';

@JsonSerializable()
class Meeting {
  final int id;
  final String title;
  @JsonKey(name: 'date_time')
  final DateTime dateTime;
  final String location;
  final int capacity;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;
  final List<UserMeeting>? participants;

  Meeting({
    required this.id,
    required this.title,
    required this.dateTime,
    required this.location,
    required this.capacity,
    required this.createdAt,
    this.participants,
  });

  factory Meeting.fromJson(Map<String, dynamic> json) =>
      _$MeetingFromJson(json);
  Map<String, dynamic> toJson() => _$MeetingToJson(this);

  // 현재 참가자 수 계산
  int get currentParticipants {
    if (participants == null) return 0;
    return participants!
        .where((p) => p.status == 'CONFIRMED' || p.status == 'PENDING')
        .length;
  }

  // 참가 가능 여부
  bool get isAvailable {
    return currentParticipants < capacity;
  }

  // 참가율 계산
  double get occupancyRate {
    if (capacity == 0) return 0.0;
    return currentParticipants / capacity;
  }
}

// 모임 생성 요청 모델
@JsonSerializable()
class MeetingCreate {
  final String title;
  @JsonKey(name: 'date_time')
  final DateTime dateTime;
  final String location;
  final int capacity;

  MeetingCreate({
    required this.title,
    required this.dateTime,
    required this.location,
    required this.capacity,
  });

  factory MeetingCreate.fromJson(Map<String, dynamic> json) =>
      _$MeetingCreateFromJson(json);
  Map<String, dynamic> toJson() => _$MeetingCreateToJson(this);
}

