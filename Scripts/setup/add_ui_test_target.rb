# Adds the NaukriGulfUITests UI test target to NaukriGulf.xcodeproj (idempotent).
# Usage: ruby add_ui_test_target.rb /path/to/NaukriGulf.xcodeproj
require 'xcodeproj'

NAME = 'NaukriGulfUITests'.freeze
project_path = ARGV[0] or abort('usage: add_ui_test_target.rb <xcodeproj>')
project = Xcodeproj::Project.open(project_path)

abort("#{NAME} already exists, nothing to do") if project.targets.any? { |t| t.name == NAME }

app = project.targets.find { |t| t.name == 'NaukriGulf' } or abort('NaukriGulf target not found')
app_debug = app.build_settings('Debug')

target = project.new_target(:ui_test_bundle, NAME, :ios, app_debug['IPHONEOS_DEPLOYMENT_TARGET'] || '13.0')
target.add_dependency(app)

# Synchronized folder: any .swift file placed in NaukriGulfUITests/ is compiled automatically.
group = project.new(Xcodeproj::Project::Object::PBXFileSystemSynchronizedRootGroup)
group.path = NAME
group.source_tree = '<group>'
project.main_group.children << group
target.file_system_synchronized_groups << group

# Mirror every project configuration (Debug/Staging/Docker/Release).
existing = target.build_configuration_list.build_configurations.map(&:name)
project.build_configurations.map(&:name).each do |cfg|
  next if existing.include?(cfg)
  base = target.build_configuration_list.build_configurations.find { |c| c.name == (cfg == 'Release' ? 'Release' : 'Debug') }
  bc = project.new(Xcodeproj::Project::Object::XCBuildConfiguration)
  bc.name = cfg
  bc.build_settings = base.build_settings.dup
  target.build_configuration_list.build_configurations << bc
end

target.build_configurations.each do |c|
  s = c.build_settings
  s['TEST_TARGET_NAME'] = 'NaukriGulf'
  s['PRODUCT_BUNDLE_IDENTIFIER'] = 'com.infoedge.NaukriGulf.UITests'
  s['PRODUCT_NAME'] = '$(TARGET_NAME)'
  s['GENERATE_INFOPLIST_FILE'] = 'YES'
  s['SWIFT_VERSION'] = app_debug['SWIFT_VERSION'] || '5.0'
  s['TARGETED_DEVICE_FAMILY'] = '1'
  s['CODE_SIGN_STYLE'] = 'Automatic'
  s['DEVELOPMENT_TEAM'] = app_debug['DEVELOPMENT_TEAM'] if app_debug['DEVELOPMENT_TEAM']
end

project.save
puts "Added #{NAME} with configs: #{target.build_configurations.map(&:name).join(', ')}"
