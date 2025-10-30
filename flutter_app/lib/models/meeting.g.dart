// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'meeting.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Meeting _$MeetingFromJson(Map<String, dynamic> json) => Meeting(
      id: (json['id'] as num).toInt(),
      title: json['title'] as String,
      dateTime: DateTime.parse(json['date_time'] as String),
      location: json['location'] as String,
      capacity: (json['capacity'] as num).toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
      participants: (json['participants'] as List<dynamic>?)
          ?.map((e) => UserMeeting.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$MeetingToJson(Meeting instance) => <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'date_time': instance.dateTime.toIso8601String(),
      'location': instance.location,
      'capacity': instance.capacity,
      'created_at': instance.createdAt.toIso8601String(),
      'participants': instance.participants,
    };

MeetingCreate _$MeetingCreateFromJson(Map<String, dynamic> json) =>
    MeetingCreate(
      title: json['title'] as String,
      dateTime: DateTime.parse(json['date_time'] as String),
      location: json['location'] as String,
      capacity: (json['capacity'] as num).toInt(),
    );

Map<String, dynamic> _$MeetingCreateToJson(MeetingCreate instance) =>
    <String, dynamic>{
      'title': instance.title,
      'date_time': instance.dateTime.toIso8601String(),
      'location': instance.location,
      'capacity': instance.capacity,
    };
