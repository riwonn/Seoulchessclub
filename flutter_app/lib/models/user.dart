import 'package:json_annotation/json_annotation.dart';
import 'meeting.dart';

part 'user.g.dart';

@JsonSerializable()
class User {
  final int id;
  final String name;
  @JsonKey(name: 'phone_number')
  final String phoneNumber;
  final String email;
  final String gender;
  @JsonKey(name: 'birth_year')
  final int? birthYear;
  @JsonKey(name: 'chess_experience')
  final String chessExperience;
  @JsonKey(name: 'chess_rating')
  final String? chessRating;
  @JsonKey(name: 'total_visits')
  final int totalVisits;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;
  @JsonKey(name: 'updated_at')
  final DateTime updatedAt;
  @JsonKey(name: 'attended_meetings')
  final List<UserMeeting>? attendedMeetings;

  User({
    required this.id,
    required this.name,
    required this.phoneNumber,
    required this.email,
    required this.gender,
    this.birthYear,
    required this.chessExperience,
    this.chessRating,
    required this.totalVisits,
    required this.createdAt,
    required this.updatedAt,
    this.attendedMeetings,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}

@JsonSerializable()
class UserMeeting {
  final int id;
  @JsonKey(name: 'user_id')
  final int userId;
  @JsonKey(name: 'meeting_id')
  final int meetingId;
  final String status;
  @JsonKey(name: 'registered_at')
  final DateTime registeredAt;

  UserMeeting({
    required this.id,
    required this.userId,
    required this.meetingId,
    required this.status,
    required this.registeredAt,
  });

  factory UserMeeting.fromJson(Map<String, dynamic> json) =>
      _$UserMeetingFromJson(json);
  Map<String, dynamic> toJson() => _$UserMeetingToJson(this);
}

// 회원가입 요청 모델
@JsonSerializable()
class UserCreate {
  final String name;
  @JsonKey(name: 'phone_number')
  final String phoneNumber;
  final String email;
  final String gender;
  @JsonKey(name: 'birth_year')
  final int? birthYear;
  @JsonKey(name: 'chess_experience')
  final String chessExperience;
  @JsonKey(name: 'chess_rating')
  final String? chessRating;

  UserCreate({
    required this.name,
    required this.phoneNumber,
    required this.email,
    required this.gender,
    this.birthYear,
    required this.chessExperience,
    this.chessRating,
  });

  factory UserCreate.fromJson(Map<String, dynamic> json) =>
      _$UserCreateFromJson(json);
  Map<String, dynamic> toJson() => _$UserCreateToJson(this);
}

// 성별 Enum
enum Gender {
  @JsonValue('MALE')
  male,
  @JsonValue('FEMALE')
  female,
  @JsonValue('OTHER')
  other,
}

// 체스 경험 Enum
enum ChessExperience {
  @JsonValue('NO_BUT_WANT_TO_LEARN')
  noButWantToLearn,
  @JsonValue('KNOW_RULES_ONLY')
  knowRulesOnly,
  @JsonValue('OCCASIONALLY_PLAY')
  occasionallyPlay,
  @JsonValue('PLAY_WELL')
  playWell,
}

// 체스 레이팅 Enum
enum ChessRating {
  @JsonValue('I_DONT_KNOW')
  iDontKnow,
  @JsonValue('UNDER_1000')
  under1000,
  @JsonValue('BETWEEN_1000_1500')
  between1000And1500,
  @JsonValue('BETWEEN_1500_2000')
  between1500And2000,
  @JsonValue('OVER_2000')
  over2000,
}

